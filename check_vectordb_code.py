import sys
sys.path.append('.')

try:
    from vector_db import ChromaVectorDB
    import inspect
    
    print("VectorDB.add_job() method metadata fields:")
    source = inspect.getsource(ChromaVectorDB.add_job)
    
    # Extract the metadata section
    lines = source.split('\\n')
    in_metadata = False
    metadata_fields = []
    
    for line in lines:
        if 'metadatas=[' in line:
            in_metadata = True
        elif in_metadata and line.strip().startswith(']'):
            break
        elif in_metadata:
            # Look for field assignments in metadata
            if ':' in line and '=' in line:
                field = line.split(':')[0].strip().strip("'")
                metadata_fields.append(field)
    
    print("Current metadata fields:", metadata_fields)
    print("")
    print("Missing 'ai_job_profile' in metadata? ", 'ai_job_profile' not in metadata_fields)
    
except Exception as e:
    print("Error:", e)
