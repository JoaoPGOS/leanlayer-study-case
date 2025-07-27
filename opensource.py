import threading
import pandas as pd
import sys
import time
import warnings
import logging
from langchain.schema import Document
from langchain.embeddings import HuggingFaceInstructEmbeddings
from langchain.vectorstores import FAISS
from langchain.llms import Ollama
from langchain.chains import RetrievalQA

# 🔇 Suppress warnings and external logs
warnings.filterwarnings("ignore")
logging.disable(logging.CRITICAL)

# Thread-safe shared list to store results
results_lock = threading.Lock()
results_list = []

# 🔒 Global lock to ensure sequential execution (one analysis at a time)
analysis_lock = threading.Lock()


def analyzing_animation(stop_event):
    """
    Animated terminal message showing that the analysis is running.
    Stops when stop_event is set.
    """
    text = "..."
    gray_shades = list(range(232, 256)) + list(range(254, 231, -1))
    shade_index = 0
    while not stop_event.is_set():
        for i in range(len(text) + 1):
            if stop_event.is_set():
                break
            shade = gray_shades[shade_index % len(gray_shades)]
            sys.stdout.write(f"\r\033[38;5;{shade}mAnalyzing{text[i:] + ' ' * i}\033[0m")
            sys.stdout.flush()
            time.sleep(0.1)
            shade_index += 1
    sys.stdout.write("\r\033[97mDone analyzing!           \033[0m\n")
    sys.stdout.flush()


def analyze_async(df: pd.DataFrame, query: str, model_name: str = "mistral", do_in_the_end=None, question=""):
    """
    Run analysis in its own thread, but only one at a time.
    Special tasks (like export) can also be queued by passing an empty df and query.
    """
    def worker():
        with analysis_lock:  # ensures sequential execution
            stop_event = threading.Event()
            anim_thread = threading.Thread(target=analyzing_animation, args=(stop_event,))
            anim_thread.start()

            try:
                if not df.empty and query.strip():  # ✅ Only run AI if it's a real analysis
                    # Convert DataFrame to LangChain Documents
                    docs = [
                        Document(page_content=" | ".join([f"{col}: {row[col]}" for col in df.columns]))
                        for _, row in df.iterrows()
                    ]

                    # Build embeddings + FAISS vectorstore
                    embeddings = HuggingFaceInstructEmbeddings(model_name="hkunlp/instructor-large")
                    vectorstore = FAISS.from_documents(docs, embeddings)

                    # Run the LLM analysis
                    llm = Ollama(model=model_name)
                    qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=vectorstore.as_retriever())
                    response = qa_chain.run(query)

                    # Save result in a thread-safe way
                    with results_lock:
                        results_list.append({
                            "question": question,
                            "query": query,
                            "answer": response
                        })

                else:
                    print("\nℹ️ Skipping AI processing (special queued task)...")

            except Exception as e:
                print(f"❌ Error in analyze_async: {e}")

            finally:
                stop_event.set()
                anim_thread.join()
                if do_in_the_end:
                    do_in_the_end()

    threading.Thread(target=worker, daemon=True).start()


# Global main DataFrame to hold questions and answers
ai_df = pd.DataFrame(columns=["question", "answer"])
def export_data():
    global ai_df
    sync_results_to_main_df()
    ai_df.to_csv("ai_results.csv", index=False)
    print("Exported")

def sync_results_to_main_df():
    global ai_df, results_list
    with results_lock:
        if results_list:
            for item in results_list:
                ai_df.loc[len(ai_df)] = [item["question"], item["answer"]]
            results_list.clear()

def get_ai_df():
    sync_results_to_main_df()
    return ai_df

def clear_ai_session():
    global ai_df, results_list
    with results_lock:
        ai_df = pd.DataFrame(columns=["question", "answer"])
        results_list.clear()
    print("AI session data cleared.")

