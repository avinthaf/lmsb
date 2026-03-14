-- Media Tables

-- Media Images Table
CREATE TABLE IF NOT EXISTS media_images (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    url TEXT NOT NULL,
    school_id UUID NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    deleted_at TIMESTAMP WITH TIME ZONE
);

-- Media Videos Table
CREATE TABLE IF NOT EXISTS media_videos (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    url TEXT NOT NULL,
    thumbnail_id UUID REFERENCES media_images(id),
    duration INTEGER NOT NULL,
    school_id UUID NOT NULL,
    category_id UUID NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    deleted_at TIMESTAMP WITH TIME ZONE
);

-- Media Tags Junction Table
CREATE TABLE IF NOT EXISTS media_tags (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tag_id UUID NOT NULL,
    media_id UUID NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    deleted_at TIMESTAMP WITH TIME ZONE
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_media_images_school_id ON media_images(school_id);
CREATE INDEX IF NOT EXISTS idx_media_images_deleted_at ON media_images(deleted_at);

CREATE INDEX IF NOT EXISTS idx_media_videos_school_id ON media_videos(school_id);
CREATE INDEX IF NOT EXISTS idx_media_videos_category_id ON media_videos(category_id);
CREATE INDEX IF NOT EXISTS idx_media_videos_thumbnail_id ON media_videos(thumbnail_id);
CREATE INDEX IF NOT EXISTS idx_media_videos_deleted_at ON media_videos(deleted_at);

CREATE INDEX IF NOT EXISTS idx_media_tags_tag_id ON media_tags(tag_id);
CREATE INDEX IF NOT EXISTS idx_media_tags_media_id ON media_tags(media_id);
CREATE INDEX IF NOT EXISTS idx_media_tags_deleted_at ON media_tags(deleted_at);

-- Triggers for updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_media_images_updated_at
    BEFORE UPDATE ON media_images
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_media_videos_updated_at
    BEFORE UPDATE ON media_videos
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_media_tags_updated_at
    BEFORE UPDATE ON media_tags
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();
