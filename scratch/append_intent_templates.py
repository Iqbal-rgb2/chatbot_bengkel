schema_path = 'database/schema_and_seed.sql'
seed_path = 'scratch/intent_templates_seed.sql'

with open(schema_path, 'r', encoding='utf-8') as f:
    schema_content = f.read()

with open(seed_path, 'r', encoding='utf-8') as f:
    seed_content = f.read()

# Locate the place to insert: right before DELETE FROM "sqlite_sequence";
target_str = 'DELETE FROM "sqlite_sequence";'
if target_str in schema_content:
    parts = schema_content.split(target_str)
    
    # We want to insert seed_content, then target_str, and insert the sequence row for intent_templates
    sequence_insert = '\nINSERT INTO "sqlite_sequence" VALUES(\'intent_templates\',294);'
    new_content = parts[0] + seed_content + '\n' + target_str + sequence_insert + parts[1]
    
    with open(schema_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("Successfully appended intent_templates to schema_and_seed.sql!")
else:
    print("Error: Target string not found in schema_and_seed.sql")
