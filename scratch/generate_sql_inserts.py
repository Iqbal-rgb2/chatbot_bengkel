import json

json_path = 'scripts/seeder_data/training_templates.json'
sql_path = 'scratch/intent_templates_seed.sql'

with open(json_path, 'r', encoding='utf-8') as f:
    templates = json.load(f)

sql_statements = []
sql_statements.append('\n-- INTENT TEMPLATES CREATE TABLE')
sql_statements.append('CREATE TABLE "intent_templates" (')
sql_statements.append('\t"id"\tINTEGER,')
sql_statements.append('\t"intent"\tTEXT NOT NULL,')
sql_statements.append('\t"template_text"\tTEXT NOT NULL,')
sql_statements.append('\tPRIMARY KEY("id" AUTOINCREMENT)')
sql_statements.append(');')

idx = 1
for intent, phrases in templates.items():
    sql_statements.append(f'\n-- Templates for: {intent}')
    for phrase in phrases:
        # Escape single quotes in phrase
        escaped_phrase = phrase.replace("'", "''")
        sql_statements.append(f"INSERT INTO \"intent_templates\" VALUES({idx}, '{intent}', '{escaped_phrase}');")
        idx += 1

with open(sql_path, 'w', encoding='utf-8') as f:
    f.write('\n'.join(sql_statements) + '\n')

print(f"Generated {idx - 1} SQL inserts in {sql_path}")
