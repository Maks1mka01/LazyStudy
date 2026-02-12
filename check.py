"""
Diagnostic Script - Run this to check what's missing
Save as check_dependencies.py and run: python check_dependencies.py
"""

import sys
import os

print("=" * 60)
print("STATISTICS PAGE DIAGNOSTIC")
print("=" * 60)

# Check files exist
print("\n📁 CHECKING FILES:")
files_to_check = [
    'app.py',
    'analytics.py',
    'visualizations.py',
    'templates/statistics.html',
    'database.py'
]

missing_files = []
for file in files_to_check:
    if os.path.exists(file):
        print(f"  ✅ {file}")
    else:
        print(f"  ❌ {file} - MISSING")
        missing_files.append(file)

# Check imports
print("\n📦 CHECKING IMPORTS:")
imports_to_check = [
    ('flask', 'Flask'),
    ('matplotlib', 'matplotlib'),
    ('numpy', 'NumPy'),
    ('database', 'database.py'),
]

missing_imports = []
for module, name in imports_to_check:
    try:
        __import__(module)
        print(f"  ✅ {name}")
    except ImportError:
        print(f"  ❌ {name} - NOT INSTALLED")
        missing_imports.append(name)

# Check analytics functions
print("\n🔧 CHECKING ANALYTICS FUNCTIONS:")
try:
    import analytics
    functions = [
        'get_study_statistics',
        'get_deck_statistics',
        'get_interval_distribution',
        'get_easiness_distribution',
        'get_upcoming_reviews',
        'calculate_retention_metrics',
        'get_numerical_statistics',
        'calculate_correlation_matrix'
    ]
    
    for func in functions:
        if hasattr(analytics, func):
            print(f"  ✅ analytics.{func}")
        else:
            print(f"  ❌ analytics.{func} - MISSING")
except ImportError as e:
    print(f"  ❌ Cannot import analytics: {e}")

# Check visualizations functions
print("\n📊 CHECKING VISUALIZATION FUNCTIONS:")
try:
    import visualizations
    functions = [
        'generate_overall_summary_chart',
        'generate_deck_progress_chart',
        'generate_interval_distribution_chart',
        'generate_difficulty_distribution_chart',
        'generate_upcoming_reviews_chart',
        'generate_retention_metrics_chart'
    ]
    
    for func in functions:
        if hasattr(visualizations, func):
            print(f"  ✅ visualizations.{func}")
        else:
            print(f"  ❌ visualizations.{func} - MISSING")
except ImportError as e:
    print(f"  ❌ Cannot import visualizations: {e}")

# Summary
print("\n" + "=" * 60)
print("SUMMARY")
print("=" * 60)

if missing_files:
    print(f"\n❌ MISSING FILES ({len(missing_files)}):")
    for file in missing_files:
        print(f"   - {file}")
    print("\n   → Copy these files from the fixes/ folder")

if missing_imports:
    print(f"\n❌ MISSING PACKAGES ({len(missing_imports)}):")
    for pkg in missing_imports:
        print(f"   - {pkg}")
    if 'matplotlib' in missing_imports:
        print("\n   → Run: pip install matplotlib")
    if 'NumPy' in missing_imports:
        print("\n   → Run: pip install numpy")

if not missing_files and not missing_imports:
    print("\n✅ ALL DEPENDENCIES FOUND!")
    print("\nIf statistics page still fails:")
    print("1. Check Python console for error messages")
    print("2. Try the minimal test route (test_statistics_minimal.txt)")
    print("3. Make sure 'import analytics' and 'import visualizations' are in app.py")

print("\n" + "=" * 60)