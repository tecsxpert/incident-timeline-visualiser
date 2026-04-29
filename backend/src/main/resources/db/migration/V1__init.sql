CREATE TABLE incident_timeline (
    id                  BIGSERIAL PRIMARY KEY,
    title               VARCHAR(255)        NOT NULL,
    description         TEXT,
    incident_type       VARCHAR(100)        NOT NULL,
    severity            VARCHAR(50)         NOT NULL,
    status              VARCHAR(50)         NOT NULL DEFAULT 'OPEN',
    reported_by         VARCHAR(150)        NOT NULL,
    assigned_to         VARCHAR(150),
    incident_date       TIMESTAMP           NOT NULL,
    resolved_date       TIMESTAMP,
    resolution_notes    TEXT,
    ai_description      TEXT,
    ai_recommendations  TEXT,
    ai_report           TEXT,
    is_deleted          BOOLEAN             NOT NULL DEFAULT FALSE,
    created_at          TIMESTAMP           NOT NULL DEFAULT NOW(),
    updated_at          TIMESTAMP           NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_incident_status      ON incident_timeline(status);
CREATE INDEX idx_incident_severity    ON incident_timeline(severity);
CREATE INDEX idx_incident_date        ON incident_timeline(incident_date);
CREATE INDEX idx_incident_type        ON incident_timeline(incident_type);
CREATE INDEX idx_incident_is_deleted  ON incident_timeline(is_deleted);
CREATE INDEX idx_incident_reported_by ON incident_timeline(reported_by);