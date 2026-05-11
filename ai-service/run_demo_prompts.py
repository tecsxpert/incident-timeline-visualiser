import sys, time, requests

BASE_URL = "http://localhost:5000"

RECORDS = [
    ("INC-001", "Production Database Complete Outage",         "SEV-1", "PostgreSQL primary, all API endpoints",          "Primary PostgreSQL became unresponsive. Disk filled to 100% due to unrotated WAL logs.",          "2025-11-01T02:14:00Z", "2025-11-01T03:47:00Z", "WAL archiving job had silently failed 6 days prior."),
    ("INC-002", "Payment Gateway Timeout Cascade",             "SEV-1", "Payment service, checkout API",                  "Gateway returned 504 timeouts. Retry storms exhausted thread pool. 100% of payments failed.",      "2025-11-14T18:03:00Z", "2025-11-14T18:44:00Z", "Third-party gateway increased internal timeout without notice."),
    ("INC-003", "SSL Certificate Expiry on API Gateway",       "SEV-1", "API gateway, all external integrations",         "Certificate expired at midnight. All HTTPS traffic rejected.",                                    "2025-10-01T00:00:00Z", "2025-10-01T01:22:00Z", "Automated renewal failed silently. No alert configured."),
    ("INC-004", "Redis Cache Cluster Full Eviction",           "SEV-1", "Redis cluster, session store",                   "All 3 Redis nodes crashed due to missing maxmemory policy. All sessions invalidated.",            "2025-09-22T11:30:00Z", "2025-09-22T12:15:00Z", "maxmemory-policy set to noeviction causing OOM crash."),
    ("INC-005", "Kubernetes Node Pool Scaling Failure",        "SEV-1", "Kubernetes cluster, all microservices",          "Autoscaler failed to provision nodes during traffic spike. All pods Pending.",                    "2025-08-09T14:45:00Z", "2025-08-09T15:13:00Z", "vCPU quota exhausted in target availability zone."),
    ("INC-006", "ETL Pipeline Data Corruption",                "SEV-1", "ETL pipeline, data warehouse",                   "Nightly ETL inserted duplicate rows. Executive reports generated with corrupt data.",             "2025-07-15T01:00:00Z", "2025-07-15T08:30:00Z", "Migration dropped a UNIQUE constraint without an application guard."),
    ("INC-007", "Elasticsearch OOM — Search Degraded",         "SEV-2", "Elasticsearch cluster, product search",         "Heap reached 98%. P99 latency spiked to 18 seconds. Search very slow.",                          "2025-11-10T09:00:00Z", "2025-11-10T11:45:00Z", "New wildcard aggregation query had O(n^2) cardinality."),
    ("INC-008", "Email Notification Backlog — 47k Messages",   "SEV-2", "Email worker, SQS queue, SMTP relay",           "Email delivery backed up to 47,000 messages. OTPs not delivered for 4 hours.",                   "2025-10-28T13:00:00Z", "2025-10-28T17:20:00Z", "Marketing bulk send routed through transactional queue."),
    ("INC-009", "JWT Validation Latency Spike",                "SEV-2", "Auth service, all protected endpoints",         "JWT validation went from 12ms to 890ms P99. Login and API calls timed out.",                     "2025-10-05T16:00:00Z", "2025-10-05T17:30:00Z", "JWKS cache TTL accidentally set to 0."),
    ("INC-010", "File Upload Failing — S3 Quota Hit",          "SEV-2", "File upload API, S3 bucket",                    "File uploads returned 500 errors. S3 bucket quota of 50GB was hit.",                            "2025-09-18T10:30:00Z", "2025-09-18T12:00:00Z", "Terraform variable for bucket quota not reverted after staging."),
    ("INC-011", "WebSocket Connections Dropping Every 60s",    "SEV-2", "WebSocket service, real-time notifications",    "All WebSocket connections dropped every 60 seconds.",                                           "2025-09-03T08:00:00Z", "2025-09-03T09:15:00Z", "ALB idle timeout set to 60 seconds — too short for WebSockets."),
    ("INC-012", "Groq Rate Limit — All AI Features Down",      "SEV-2", "AI microservice, all AI endpoints",            "Groq API rate limit exhausted. All AI endpoints returned fallback responses for 90 minutes.",    "2025-08-20T14:00:00Z", "2025-08-20T15:30:00Z", "Load test script pointed at PROD_BASE_URL instead of staging."),
    ("INC-013", "Flyway Checksum Mismatch — App Won't Start",  "SEV-2", "Backend API, Spring Boot, all endpoints",      "Deployment failed. App refused to start due to Flyway checksum mismatch.",                       "2025-07-28T11:00:00Z", "2025-07-28T12:45:00Z", "Developer edited a committed migration file after it was applied."),
    ("INC-014", "CDN Serving Stale Pricing Data",              "SEV-2", "CDN, product catalogue API, pricing service",  "CDN served stale pricing for 2 hours after a price update.",                                    "2025-07-10T09:00:00Z", "2025-07-10T11:00:00Z", "Pricing API did not set Cache-Control headers."),
    ("INC-015", "Scheduled Reports Not Generated for 2 Weeks", "SEV-3", "Report scheduler, PDF service",               "Weekly executive reports not generated for two consecutive weeks.",                             "2025-11-03T06:00:00Z", "2025-11-17T10:00:00Z", "REPORT_BUCKET env var missing after infrastructure migration."),
    ("INC-016", "Pagination Returns Wrong Results",            "SEV-3", "Incidents list API, frontend dashboard",       "Page 2 returned same results as page 1 for datasets over 1,000 records.",                      "2025-10-22T09:00:00Z", "2025-10-22T15:00:00Z", "OFFSET pagination with inconsistent ORDER BY."),
    ("INC-017", "Audit Log Missing All DELETE Operations",     "SEV-3", "Audit logging, compliance reports",            "All DELETE operations missing from audit logs for 3 weeks.",                                   "2025-09-29T00:00:00Z", "2025-10-20T14:00:00Z", "AOP pointcut pattern used old package name after refactor."),
    ("INC-018", "CSV Export Corrupts Non-ASCII Characters",    "SEV-3", "CSV export endpoint",                          "Exported CSV files showed garbled characters for accented or CJK titles.",                     "2025-09-12T00:00:00Z", "2025-09-12T14:00:00Z", "Content-Type header missing charset=UTF-8."),
    ("INC-019", "Docker Health Check Always Returns Healthy",  "SEV-3", "Docker Compose, container orchestration",      "AI service reported healthy while Flask was in error state.",                                   "2025-08-25T00:00:00Z", "2025-08-25T11:00:00Z", "/health endpoint did not check Groq client or ChromaDB."),
    ("INC-020", "Swagger UI Showing Stale API Contracts",      "SEV-3", "Swagger UI, API docs",                         "Frontend team made 6 failed integration attempts based on stale Swagger docs.",                 "2025-08-11T00:00:00Z", "2025-08-11T16:00:00Z", "OpenAPI annotations not updated when endpoint contracts changed."),
    ("INC-021", "Rate Limiter Blocking Enterprise Users",      "SEV-3", "Flask rate limiter, AI service",              "Multiple enterprise users behind corporate NAT hit 30 req/min limit within seconds.",           "2025-07-30T10:00:00Z", "2025-07-30T15:00:00Z", "Rate limiting keyed on remote IP only."),
    ("INC-022", "Soft-Deleted Records Appearing in Search",    "SEV-3", "Search API, incident list",                   "Soft-deleted incidents visible in search results and dashboard counts.",                       "2025-07-18T00:00:00Z", "2025-07-18T13:00:00Z", "@Where annotation not applied in JPQL JOIN FETCH."),
    ("INC-023", "Dashboard KPI Cards Showing Yesterday Data",  "SEV-4", "Dashboard, /stats endpoint, Redis cache",     "KPI cards showed counts 24 hours stale.",                                                       "2025-11-08T09:00:00Z", "2025-11-08T11:30:00Z", "Cache TTL set to 86400 seconds instead of 600."),
    ("INC-024", "Login Error Message Reveals Valid Accounts",  "SEV-4", "Auth service, login endpoint",               "Login returned different messages for unknown email vs wrong password.",                        "2025-10-30T00:00:00Z", "2025-10-30T16:00:00Z", "AuthController returned distinct errors per case."),
    ("INC-025", "Double-Submit Creates Duplicate Incidents",   "SEV-4", "React frontend, incident create form",        "Submit button not disabled during API call. Double-click created duplicates.",                  "2025-10-15T00:00:00Z", "2025-10-15T14:00:00Z", "Frontend form had no submitting state."),
    ("INC-026", "Table Overflows on 768px Tablet Viewport",    "SEV-4", "React frontend, incident list table",        "Incidents table overflowed horizontally on tablet viewports.",                                  "2025-09-25T00:00:00Z", "2025-09-25T15:00:00Z", "Table column widths hardcoded in px."),
    ("INC-027", "README Missing CHROMA_PERSIST_DIR Variable",  "SEV-4", "Documentation, developer onboarding",        "New developers could not start AI service. CHROMA_PERSIST_DIR missing from .env.example.",       "2025-09-10T00:00:00Z", "2025-09-10T12:00:00Z", "Variable added to codebase without updating .env.example."),
    ("INC-028", "AI Cache Key Collision — Wrong Response",     "SEV-4", "AI cache, Redis, /describe endpoint",        "Two incidents with similar titles got the same cache key and wrong response.",                  "2025-08-28T00:00:00Z", "2025-08-28T13:00:00Z", "Cache key only hashed title and severity, not full payload."),
    ("INC-029", "Incident Times Show Wrong Timezone",          "SEV-4", "Frontend timeline view",                     "Incident times displayed in browser local timezone with no UTC label.",                        "2025-08-05T00:00:00Z", "2025-08-05T11:00:00Z", "Frontend used toLocaleString() without UTC label."),
    ("INC-030", "Stale ChromaDB Embeddings After Model Upgrade","SEV-4","AI service, ChromaDB",                       "After upgrading sentence-transformers, existing embeddings produced wrong similarity scores.",  "2025-07-22T00:00:00Z", "2025-07-22T16:00:00Z", "Collection not cleared and re-seeded after model upgrade."),
]


def post(path, payload):
    try:
        r = requests.post(f"{BASE_URL}{path}", json=payload, timeout=30)
        return r.json(), r.status_code
    except Exception as e:
        return {"error": str(e)}, 0


passed = 0
failed = 0
failures = []

print(f"\nTesting {len(RECORDS)} records against 3 endpoints...\n")

for rec in RECORDS:
    id, title, severity, systems, desc, start, end, root_cause = rec
    print(f"{id} | {severity} | {title[:45]}")

    # /ai/describe
    resp, status = post("/ai/describe", {"title": title, "severity": severity, "affected_systems": systems, "description": desc, "start_time": start, "end_time": end})
    if status == 200 and not resp.get("is_fallback"):
        print("  /describe     ✅")
        passed += 1
    else:
        print(f"  /describe     ❌  status={status}  fallback={resp.get('is_fallback')}  err={resp.get('error','')}")
        failed += 1
        failures.append(f"{id} /describe: {resp.get('error', 'fallback or bad status')}")

    # /ai/recommend
    resp, status = post("/ai/recommend", {"title": title, "severity": severity, "affected_systems": systems, "root_cause": root_cause})
    if status == 200 and not resp.get("is_fallback"):
        print("  /recommend    ✅")
        passed += 1
    else:
        print(f"  /recommend    ❌  status={status}  fallback={resp.get('is_fallback')}  err={resp.get('error','')}")
        failed += 1
        failures.append(f"{id} /recommend: {resp.get('error', 'fallback or bad status')}")

    # /ai/generate-report
    resp, status = post("/ai/generate-report", {"incident_id": id, "title": title, "severity": severity, "affected_systems": systems, "description": desc, "start_time": start, "end_time": end})
    if status == 200 and not resp.get("is_fallback"):
        print("  /gen-report   ✅")
        passed += 1
    else:
        print(f"  /gen-report   ❌  status={status}  fallback={resp.get('is_fallback')}  err={resp.get('error','')}")
        failed += 1
        failures.append(f"{id} /generate-report: {resp.get('error', 'fallback or bad status')}")

    time.sleep(0.5)  # stay under 30 req/min rate limit

print(f"\n{'='*50}")
print(f"PASSED: {passed}   FAILED: {failed}   TOTAL: {passed+failed}")
if failures:
    print("\nFailures:")
    for f in failures:
        print(f"  {f}")
    print("\nFix failures before Demo Day.")
    sys.exit(1)
else:
    print("\nAll outputs DEMO-READY ✅")
    sys.exit(0)