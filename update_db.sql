-- Add new columns to progress table
ALTER TABLE progress ADD COLUMN IF NOT EXISTS is_favorite BOOLEAN DEFAULT FALSE;
ALTER TABLE progress ADD COLUMN IF NOT EXISTS engagement_rating INTEGER;
ALTER TABLE progress ADD COLUMN IF NOT EXISTS access_count INTEGER DEFAULT 1;
ALTER TABLE progress ADD COLUMN IF NOT EXISTS last_session_duration INTEGER;
ALTER TABLE progress ADD COLUMN IF NOT EXISTS average_session_time FLOAT;
ALTER TABLE progress ADD COLUMN IF NOT EXISTS streak_count INTEGER DEFAULT 0;
ALTER TABLE progress ADD COLUMN IF NOT EXISTS last_streak_date DATE;
ALTER TABLE progress ADD COLUMN IF NOT EXISTS error_count INTEGER DEFAULT 0;
ALTER TABLE progress ADD COLUMN IF NOT EXISTS last_error VARCHAR(256);

-- Add new columns to sessions table
ALTER TABLE sessions ADD COLUMN IF NOT EXISTS ip_address VARCHAR(45);
ALTER TABLE sessions ADD COLUMN IF NOT EXISTS user_agent VARCHAR(255);
ALTER TABLE sessions ADD COLUMN IF NOT EXISTS device_type VARCHAR(32);

-- Create milestones table for achievement tracking
CREATE TABLE IF NOT EXISTS milestones (
    id SERIAL PRIMARY KEY,
    child_id INTEGER NOT NULL REFERENCES children(id) ON DELETE CASCADE,
    milestone_type VARCHAR(32) NOT NULL, -- 'daily', 'weekly', 'streak', 'completion', etc.
    milestone_id VARCHAR(64) NOT NULL, -- Unique identifier for the milestone
    milestone_name VARCHAR(128) NOT NULL, -- Display name
    milestone_description VARCHAR(256), -- Detailed description
    progress INTEGER DEFAULT 0, -- Current progress
    target_value INTEGER NOT NULL, -- Goal to achieve
    completed BOOLEAN DEFAULT FALSE, -- Whether milestone is completed
    earned_at TIMESTAMP, -- When milestone was completed
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (child_id, milestone_id)
);

-- Create events table for custom event tracking
CREATE TABLE IF NOT EXISTS events (
    id SERIAL PRIMARY KEY,
    user_type VARCHAR(10) NOT NULL, -- 'parent' or 'child'
    user_id INTEGER NOT NULL,
    event_type VARCHAR(64) NOT NULL, -- Type of event
    event_name VARCHAR(128) NOT NULL, -- Name of event
    event_data JSONB, -- Additional event data
    occurred_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    session_id INTEGER REFERENCES sessions(id) ON DELETE SET NULL
);

-- Add display_name column to parents table if it doesn't exist
DO $$ 
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'parents' AND column_name = 'display_name'
    ) THEN
        ALTER TABLE parents ADD COLUMN display_name VARCHAR(128);
    END IF;
END $$;

-- Create error_logs table for error tracking
CREATE TABLE IF NOT EXISTS error_logs (
    id SERIAL PRIMARY KEY,
    user_type VARCHAR(10), -- 'parent', 'child', or NULL for system errors
    user_id INTEGER,
    error_type VARCHAR(64) NOT NULL, -- Type of error
    error_message TEXT NOT NULL, -- Error message
    error_context JSONB, -- Context data when error occurred
    stack_trace TEXT, -- Stack trace if available
    occurred_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    session_id INTEGER REFERENCES sessions(id) ON DELETE SET NULL,
    resolved BOOLEAN DEFAULT FALSE,
    resolution_notes TEXT
);

-- Index for faster queries
CREATE INDEX IF NOT EXISTS idx_progress_child_content ON progress(child_id, content_type, content_id);
CREATE INDEX IF NOT EXISTS idx_progress_is_favorite ON progress(child_id, is_favorite) WHERE is_favorite = TRUE;
CREATE INDEX IF NOT EXISTS idx_milestones_child_completed ON milestones(child_id, completed);
CREATE INDEX IF NOT EXISTS idx_events_user ON events(user_type, user_id, event_type);