# API endpoint routes

from flask import Blueprint, request, jsonify
from app import db
from app.models import Trail, Feature, TrailLog, TrailSection, Wildlife  # Import relevant models

# Blueprint for API routes
api_blueprint = Blueprint('api', __name__)

# TRAIL ENDPOINTS

# 1. POST /api/trail - Create a new trail
@api_blueprint.route('/trail', methods=['POST'])
def create_trail():
    # Parse the JSON data from the request
    data = request.get_json()

    # Validate required fields
    required_fields = ['Name', 'Distance', 'EstimatedTime', 'Type']
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400

    try:
        # Create a new Trail object
        new_trail = Trail(
            Name=data['Name'],
            Description=data.get('Description'),  # Optional field
            Distance=data['Distance'],
            ElevationGain=data.get('ElevationGain'),  # Optional field
            EstimatedTime=data['EstimatedTime'],
            Type=data['Type']
        )

        # Add and commit to the database
        db.session.add(new_trail)
        db.session.commit()

        return jsonify({"message": "Trail created", "TrailID": new_trail.TrailID}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400



# 2. GET /api/trail/<TrailID> - Fetch a specific trail
@api_blueprint.route('/trail/<int:trail_id>', methods=['GET'])
def get_trail(trail_id):
    trail = Trail.query.get(trail_id)
    if not trail:
        return jsonify({"error": "Trail not found"}), 404
    return jsonify({
        "TrailID": trail.TrailID,
        "Name": trail.Name,
        "Description": trail.Description,
        "Distance": trail.Distance,
        "ElevationGain": trail.ElevationGain,
        "EstimatedTime": trail.EstimatedTime,
        "Type": trail.Type
    })

@api_blueprint.route('/trail', methods=['GET'])
def get_all_trails():
    # Fetch all trails from the database
    trails = Trail.query.all()
    # Return a JSON list of all trails
    return jsonify([{
        "TrailID": trail.TrailID,
        "Name": trail.Name,
        "Description": trail.Description,
        "Distance": trail.Distance,
        "ElevationGain": trail.ElevationGain,
        "EstimatedTime": trail.EstimatedTime,
        "Type": trail.Type
    } for trail in trails])


# 4. PUT /api/trail/<TrailID> - Update a trail
@api_blueprint.route('/trail/<int:trail_id>', methods=['PUT'])
def update_trail(trail_id):
    trail = Trail.query.get(trail_id)
    if not trail:
        return jsonify({"error": "Trail not found"}), 404

    data = request.get_json()
    try:
        trail.Name = data.get('Name', trail.Name)
        trail.Description = data.get('Description', trail.Description)
        trail.Distance = data.get('Distance', trail.Distance)
        trail.ElevationGain = data.get('ElevationGain', trail.ElevationGain)
        trail.EstimatedTime = data.get('EstimatedTime', trail.EstimatedTime)
        trail.Type = data.get('Type', trail.Type)
        db.session.commit()
        return jsonify({"message": "Trail updated"})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# 5. DELETE /api/trail/<TrailID> - Delete a trail
@api_blueprint.route('/trail/<int:trail_id>', methods=['DELETE'])
def delete_trail(trail_id):
    # Find the trail by ID
    trail = Trail.query.get(trail_id)
    if not trail:
        # Return a 404 error if the trail doesn't exist
        return jsonify({"error": f"Trail with ID {trail_id} not found"}), 404
    try:
        # Delete the trail
        db.session.delete(trail)
        db.session.commit()
        return jsonify({"message": f"Trail with ID {trail_id} deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400




# CRUD Endpoints for TrailLog

@api_blueprint.route('/traillog', methods=['POST'])
def create_traillog():
    data = request.get_json()
    try:
        new_log = TrailLog(
            TrailID=data['TrailID'],
            TrailName=data['TrailName'],
            AddedBy=data['AddedBy'],
            AddedTimestamp=data['AddedTimestamp']
        )
        db.session.add(new_log)
        db.session.commit()
        return jsonify({"message": "Trail log created", "LogID": new_log.LogID}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@api_blueprint.route('/traillog/<int:log_id>', methods=['GET'])
def get_traillog(log_id):
    log = TrailLog.query.get(log_id)
    if not log:
        return jsonify({"error": "Trail log not found"}), 404
    return jsonify({
        "LogID": log.LogID,
        "TrailID": log.TrailID,
        "TrailName": log.TrailName,
        "AddedBy": log.AddedBy,
        "AddedTimestamp": log.AddedTimestamp
    })


@api_blueprint.route('/traillog', methods=['GET'])
def get_all_traillogs():
    logs = TrailLog.query.all()
    return jsonify([{
        "LogID": log.LogID,
        "TrailID": log.TrailID,
        "TrailName": log.TrailName,
        "AddedBy": log.AddedBy,
        "AddedTimestamp": log.AddedTimestamp
    } for log in logs])


@api_blueprint.route('/traillog/<int:log_id>', methods=['PUT'])
def update_traillog(log_id):
    log = TrailLog.query.get(log_id)
    if not log:
        return jsonify({"error": "Trail log not found"}), 404

    data = request.get_json()
    try:
        log.TrailID = data.get('TrailID', log.TrailID)
        log.TrailName = data.get('TrailName', log.TrailName)
        log.AddedBy = data.get('AddedBy', log.AddedBy)
        log.AddedTimestamp = data.get('AddedTimestamp', log.AddedTimestamp)
        db.session.commit()
        return jsonify({"message": "Trail log updated"})
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@api_blueprint.route('/traillog/<int:log_id>', methods=['DELETE'])
def delete_traillog(log_id):
    log = TrailLog.query.get(log_id)
    if not log:
        return jsonify({"error": "Trail log not found"}), 404
    try:
        db.session.delete(log)
        db.session.commit()
        return jsonify({"message": "Trail log deleted"})
    except Exception as e:
        return jsonify({"error": str(e)}), 400



# CRUD Endpoints for TrailSection

@api_blueprint.route('/trailsection', methods=['POST'])
def create_trailsection():
    data = request.get_json()
    try:
        new_section = TrailSection(
            TrailID=data['TrailID'],
            SectionName=data['SectionName'],
            Distance=data['Distance'],
            DifficultyLevel=data.get('DifficultyLevel'),
            TerrainType=data.get('TerrainType')
        )
        db.session.add(new_section)
        db.session.commit()
        return jsonify({"message": "Trail section created", "SectionID": new_section.SectionID}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@api_blueprint.route('/trailsection/<int:section_id>', methods=['GET'])
def get_trailsection(section_id):
    section = TrailSection.query.get(section_id)
    if not section:
        return jsonify({"error": "Trail section not found"}), 404
    return jsonify({
        "SectionID": section.SectionID,
        "TrailID": section.TrailID,
        "SectionName": section.SectionName,
        "Distance": section.Distance,
        "DifficultyLevel": section.DifficultyLevel,
        "TerrainType": section.TerrainType
    })


@api_blueprint.route('/trailsection', methods=['GET'])
def get_all_trailsections():
    sections = TrailSection.query.all()
    return jsonify([{
        "SectionID": section.SectionID,
        "TrailID": section.TrailID,
        "SectionName": section.SectionName,
        "Distance": section.Distance,
        "DifficultyLevel": section.DifficultyLevel,
        "TerrainType": section.TerrainType
    } for section in sections])


@api_blueprint.route('/trailsection/<int:section_id>', methods=['PUT'])
def update_trailsection(section_id):
    section = TrailSection.query.get(section_id)
    if not section:
        return jsonify({"error": "Trail section not found"}), 404

    data = request.get_json()
    try:
        section.TrailID = data.get('TrailID', section.TrailID)
        section.SectionName = data.get('SectionName', section.SectionName)
        section.Distance = data.get('Distance', section.Distance)
        section.DifficultyLevel = data.get('DifficultyLevel', section.DifficultyLevel)
        section.TerrainType = data.get('TerrainType', section.TerrainType)
        db.session.commit()
        return jsonify({"message": "Trail section updated"})
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@api_blueprint.route('/trailsection/<int:section_id>', methods=['DELETE'])
def delete_trailsection(section_id):
    section = TrailSection.query.get(section_id)
    if not section:
        return jsonify({"error": "Trail section not found"}), 404
    try:
        db.session.delete(section)
        db.session.commit()
        return jsonify({"message": "Trail section deleted"})
    except Exception as e:
        return jsonify({"error": str(e)}), 400


# CRUD Endpoints for Wildlife

@api_blueprint.route('/wildlife', methods=['POST'])
def create_wildlife():
    data = request.get_json()
    try:
        new_wildlife = Wildlife(
            TrailID=data['TrailID'],
            SpeciesName=data['SpeciesName'],
            Frequency=data.get('Frequency'),
            Description=data.get('Description')
        )
        db.session.add(new_wildlife)
        db.session.commit()
        return jsonify({"message": "Wildlife entry created", "SightingID": new_wildlife.SightingID}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@api_blueprint.route('/wildlife/<int:sighting_id>', methods=['GET'])
def get_wildlife(sighting_id):
    wildlife = Wildlife.query.get(sighting_id)
    if not wildlife:
        return jsonify({"error": "Wildlife entry not found"}), 404
    return jsonify({
        "SightingID": wildlife.SightingID,
        "TrailID": wildlife.TrailID,
        "SpeciesName": wildlife.SpeciesName,
        "Frequency": wildlife.Frequency,
        "Description": wildlife.Description
    })


@api_blueprint.route('/wildlife', methods=['GET'])
def get_all_wildlife():
    wildlife_entries = Wildlife.query.all()
    return jsonify([{
        "SightingID": wildlife.SightingID,
        "TrailID": wildlife.TrailID,
        "SpeciesName": wildlife.SpeciesName,
        "Frequency": wildlife.Frequency,
        "Description": wildlife.Description
    } for wildlife in wildlife_entries])


@api_blueprint.route('/wildlife/<int:sighting_id>', methods=['PUT'])
def update_wildlife(sighting_id):
    wildlife = Wildlife.query.get(sighting_id)
    if not wildlife:
        return jsonify({"error": "Wildlife entry not found"}), 404

    data = request.get_json()
    try:
        wildlife.TrailID = data.get('TrailID', wildlife.TrailID)
        wildlife.SpeciesName = data.get('SpeciesName', wildlife.SpeciesName)
        wildlife.Frequency = data.get('Frequency', wildlife.Frequency)
        wildlife.Description = data.get('Description', wildlife.Description)
        db.session.commit()
        return jsonify({"message": "Wildlife entry updated"})
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@api_blueprint.route('/wildlife/<int:sighting_id>', methods=['DELETE'])
def delete_wildlife(sighting_id):
    wildlife = Wildlife.query.get(sighting_id)
    if not wildlife:
        return jsonify({"error": "Wildlife entry not found"}), 404
    try:
        db.session.delete(wildlife)
        db.session.commit()
        return jsonify({"message": "Wildlife entry deleted"})
    except Exception as e:
        return jsonify({"error": str(e)}), 400
