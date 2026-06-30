import pathlib

p = pathlib.Path('lib/shared/error/app_error_handler.dart')
text = p.read_text(encoding='utf-8')

old = """import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:postgrest/postgrest.dart';
import 'package:supabase_flutter/supabase_flutter.dart';"""
new = """import 'package:flutter/material.dart';
import 'package:supabase_flutter/supabase_flutter.dart';"""
if old not in text:
    raise SystemExit("Import anchor not found - aborting, no changes made.")
text = text.replace(old, new, 1)

p.write_text(text, encoding='utf-8')
print("app_error_handler.dart: removed redundant imports.")