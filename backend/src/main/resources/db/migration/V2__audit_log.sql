CREATE TABLE audit_log (
    id              BIGSERIAL PRIMARY KEY,
    action          VARCHAR(50)     NOT NULL,
    entity_name     VARCHAR(100)    NOT NULL,
    entity_id       BIGINT,
    performed_by    VARCHAR(150)    NOT NULL,
    details         TEXT,
    created_at      TIMESTAMP       NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_audit_entity    ON audit_log(entity_name);
CREATE INDEX idx_audit_action    ON audit_log(action);
CREATE INDEX idx_audit_performed ON audit_log(performed_by);