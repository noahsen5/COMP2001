# SQLAlchemy models for database tables


from app import db

# Trail Table
class Trail(db.Model):
    __tablename__ = 'Trail'
    __table_args__ = {'schema': 'CW2'}

    TrailID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Name = db.Column(db.String(100), nullable=False)
    Description = db.Column(db.String(255), nullable=True)
    Distance = db.Column(db.Float, nullable=False)
    ElevationGain = db.Column(db.Integer, nullable=True)
    EstimatedTime = db.Column(db.String(50), nullable=True)
    Type = db.Column(db.String(50), nullable=True)

# Feature Table (example for related tables)
class Feature(db.Model):
    __tablename__ = 'Feature'
    __table_args__ = {'schema': 'CW2'}

    FeatureID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    TrailID = db.Column(db.Integer, db.ForeignKey('CW2.Trail.TrailID'), nullable=False)
    FeatureType = db.Column(db.String(150), nullable=False)



class TrailLog(db.Model):
    __tablename__ = 'TrailLog'
    __table_args__ = {'schema': 'CW2'}

    LogID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    TrailID = db.Column(db.Integer, db.ForeignKey('CW2.Trail.TrailID'), nullable=False)
    TrailName = db.Column(db.String(100), nullable=False)
    AddedBy = db.Column(db.String(100), nullable=False)
    AddedTimestamp = db.Column(db.DateTime, nullable=False)

    # Relationships (Optional)
    trail = db.relationship('Trail', backref='logs', lazy=True)


class TrailSection(db.Model):
    __tablename__ = 'TrailSection'
    __table_args__ = {'schema': 'CW2'}

    SectionID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    TrailID = db.Column(db.Integer, db.ForeignKey('CW2.Trail.TrailID'), nullable=False)
    SectionName = db.Column(db.String(100), nullable=False)
    Distance = db.Column(db.Float, nullable=False)
    DifficultyLevel = db.Column(db.String(50), nullable=True)
    TerrainType = db.Column(db.String(100), nullable=True)

    # Relationships (Optional)
    trail = db.relationship('Trail', backref='sections', lazy=True)


class Wildlife(db.Model):
    __tablename__ = 'Wildlife'
    __table_args__ = {'schema': 'CW2'}

    SightingID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    TrailID = db.Column(db.Integer, db.ForeignKey('CW2.Trail.TrailID'), nullable=False)
    SpeciesName = db.Column(db.String(100), nullable=False)
    Frequency = db.Column(db.String(50), nullable=True)
    Description = db.Column(db.Text, nullable=True)

    # Relationships (Optional)
    trail = db.relationship('Trail', backref='wildlife', lazy=True)
