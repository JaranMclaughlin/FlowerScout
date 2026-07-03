import pathlib

p = pathlib.Path('test/shared/analytics_data_test.dart')
text = p.read_text(encoding='utf-8')

old = """    test('since() resolves correctly for each period', () {
      const today = AnalyticsFilter(period: 'today');
      const days30 = AnalyticsFilter(period: '30days');
      const days90 = AnalyticsFilter(period: '3months');
      const days7 = AnalyticsFilter(period: '7days');

      final now = DateTime.now();
      expect(today.since.day, now.day);
      expect(today.since.hour, 0);
      expect(now.difference(days30.since).inDays, 30);
      expect(now.difference(days90.since).inDays, 90);
      expect(now.difference(days7.since).inDays, 7);
    });"""

new = """    test('since() resolves correctly for each period', () {
      const today = AnalyticsFilter(period: 'today');
      const days30 = AnalyticsFilter(period: '30days');
      const days90 = AnalyticsFilter(period: '3months');
      const days7 = AnalyticsFilter(period: '7days');

      final now = DateTime.now();
      // Use hour=0 check for today (not .day, which could flip at midnight)
      expect(today.since.hour, 0);
      expect(today.since.minute, 0);
      // Use inHours with tolerance for the other periods to avoid
      // flakiness from the tiny time difference between now() calls.
      expect(now.difference(days30.since).inHours, closeTo(30 * 24, 1));
      expect(now.difference(days90.since).inHours, closeTo(90 * 24, 1));
      expect(now.difference(days7.since).inHours, closeTo(7 * 24, 1));
    });"""

if old not in text:
    raise SystemExit("Anchor not found - aborting, no changes made.")
text = text.replace(old, new, 1)

p.write_text(text, encoding='utf-8')
print("Fixed flaky since() test: using inHours with tolerance instead of inDays.")