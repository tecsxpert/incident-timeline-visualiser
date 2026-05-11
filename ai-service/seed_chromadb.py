import os, sys, logging
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv
from services.embeddings_services import load_model, init_chroma
import services.embeddings_services as emb

load_dotenv()
logging.basicConfig(level=logging.INFO)

DOCUMENTS = [
    ("doc_001", "Severity levels: SEV-1 is full outage, resolve in 1 hour. SEV-2 is major feature down, resolve in 4 hours. SEV-3 is minor degradation, resolve in 24 hours. SEV-4 is cosmetic issue, resolve in 72 hours."),
    ("doc_002", "Database outage steps: Check disk space and active connections. Archive WAL logs if disk is full. Kill idle connections if limit is hit. Run VACUUM ANALYZE after recovery."),
    ("doc_003", "API gateway failure: Confirm with external ping. Check SSL certificate expiry. Reload nginx config before full restart. Switch DNS to backup region if unrecoverable."),
    ("doc_004", "Post-incident review must be completed within 48 hours for SEV-1 and SEV-2. Include: summary, UTC timeline, root cause, impact, and action items with owners and due dates."),
    ("doc_005", "During SEV-1 post updates every 15 minutes in Slack: incident ID, status, user impact, ETA, lead name. Always send an all-clear message once resolved."),
    ("doc_006", "Every production service needs: health check every 30 seconds, P99 latency alert above 2000ms, error rate alert above 1%, CPU above 85% warning, disk above 95% page."),
    ("doc_007", "Security incidents: Unauthorised access — revoke sessions and rotate credentials. Data breach — isolate systems and notify Legal within 1 hour. DDoS — enable rate limiting."),
    ("doc_008", "All production changes need a rollback plan, health check within 5 minutes post-deploy, and monitoring review for 30 minutes after. Freeze deployments during high-traffic periods."),
    ("doc_009", "Root cause analysis: Use 5 Whys by asking why five times until you reach a process flaw. Always use UTC timestamps in all RCA documentation."),
    ("doc_010", "SLO targets: API availability >= 99.9%. API P99 latency < 500ms. When 50% of error budget is consumed freeze new deployments. All SEV-1 incidents trigger an SLA breach review."),
]

load_model()
init_chroma()

if emb.model is None or emb.collection is None:
    print("ERROR: Model or ChromaDB failed to load. Check logs above.")
    sys.exit(1)

ids        = [d[0] for d in DOCUMENTS]
texts      = [d[1] for d in DOCUMENTS]
metadatas  = [{"category": "knowledge"} for _ in DOCUMENTS]

embeddings = emb.model.encode(texts, show_progress_bar=True).tolist()
emb.collection.upsert(ids=ids, documents=texts, embeddings=embeddings, metadatas=metadatas)

print(f"Done. {emb.collection.count()} documents in ChromaDB.")