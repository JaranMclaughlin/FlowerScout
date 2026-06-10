const fs = require('fs');
const f = 'C:/Users/Jaran.Mclauglin/Desktop/FlowerScout/mobile/lib/features/reports/presentation/reports_screen.dart';
let c = fs.readFileSync(f, 'utf8').replace(/\r\n/g, '\n');

// ── PATCH 1: Add design tokens after imports ──
const importEnd = "import 'package:fl_chart/fl_chart.dart';";
if (!c.includes('class _T {')) {
  c = c.replace(importEnd, importEnd + `

class _T {
  static const bg         = Color(0xFFF4F6F4);
  static const surface    = Color(0xFFFFFFFF);
  static const surfaceAlt = Color(0xFFF0F4F0);
  static const green      = Color(0xFF2D6A2D);
  static const greenLight = Color(0xFF4A9E4A);
  static const greenMint  = Color(0xFFE8F5E8);
  static const red        = Color(0xFFB53030);
  static const redLight   = Color(0xFFFFF0F0);
  static const amber      = Color(0xFF9A5C00);
  static const amberLight = Color(0xFFFFF8EC);
  static const blue       = Color(0xFF1A5FAA);
  static const blueLight  = Color(0xFFEEF4FF);
  static const ink        = Color(0xFF1A1F1A);
  static const inkMid     = Color(0xFF4A5448);
  static const inkLight   = Color(0xFF8A9688);
  static const border     = Color(0xFFE2E8E2);
  static const gold       = Color(0xFFB8860B);
  static const silver     = Color(0xFF808080);
  static const bronze     = Color(0xFF8B4513);
  static const r8  = Radius.circular(8);
  static const r12 = Radius.circular(12);
  static const r16 = Radius.circular(16);
  static const r20 = Radius.circular(20);
  static const r24 = Radius.circular(24);
}`);
}

console.log('Patch 1 done. _T class added:', c.includes('class _T {'));

// ── PATCH 2: Replace background color ──
c = c.replace("color: const Color(0xFFF6F8F7),", "color: _T.bg,");

// ── PATCH 3: Replace _dropdown widget ──
c = c.replace(
`    return DropdownButtonFormField<String>(
      value: value,
      isExpanded: true,
      decoration: InputDecoration(
        labelText: label,
        border: OutlineInputBorder(borderRadius: BorderRadius.circular(12)),
        contentPadding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
        isDense: true,
      ),
      items: items.map((e) => DropdownMenuItem(value: e, child: Text(e, overflow: TextOverflow.ellipsis))).toList(),
      onChanged: onChanged,
    );`,
`    return DropdownButtonFormField<String>(
      value: value,
      isExpanded: true,
      decoration: InputDecoration(
        labelText: label,
        labelStyle: const TextStyle(fontSize: 11, color: _T.inkLight),
        border: OutlineInputBorder(borderRadius: const BorderRadius.all(_T.r12), borderSide: const BorderSide(color: _T.border)),
        enabledBorder: OutlineInputBorder(borderRadius: const BorderRadius.all(_T.r12), borderSide: const BorderSide(color: _T.border)),
        focusedBorder: OutlineInputBorder(borderRadius: const BorderRadius.all(_T.r12), borderSide: const BorderSide(color: _T.green, width: 1.5)),
        contentPadding: const EdgeInsets.symmetric(horizontal: 10, vertical: 8),
        isDense: true,
        filled: true,
        fillColor: _T.surface,
      ),
      style: const TextStyle(fontSize: 12, color: _T.ink, fontWeight: FontWeight.w500),
      items: items.map((e) => DropdownMenuItem(value: e, child: Text(e, overflow: TextOverflow.ellipsis))).toList(),
      onChanged: onChanged,
    );`
);

// ── PATCH 4: Replace stat card internals ──
c = c.replace(
`        padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 8),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Container(
              padding: const EdgeInsets.all(6),
              decoration: BoxDecoration(color: color.withValues(alpha: 0.12), borderRadius: BorderRadius.circular(10)),
              child: Icon(icon, size: 18, color: color),
            ),
            const SizedBox(height: 4),
            Text('$value', style: const TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
            const SizedBox(height: 1),
            Text(label, style: const TextStyle(fontSize: 10, color: Colors.grey)),
            const SizedBox(height: 3),`,
`        padding: const EdgeInsets.all(10),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          mainAxisSize: MainAxisSize.min,
          children: [
            Row(
              children: [
                Container(
                  padding: const EdgeInsets.all(5),
                  decoration: BoxDecoration(color: color.withValues(alpha: 0.12), borderRadius: const BorderRadius.all(_T.r8)),
                  child: Icon(icon, size: 14, color: color),
                ),
                const Spacer(),
                Container(
                  padding: const EdgeInsets.symmetric(horizontal: 5, vertical: 2),
                  decoration: BoxDecoration(
                    color: trendUp ? const Color(0xFFE8F5E8) : const Color(0xFFFFF0F0),
                    borderRadius: const BorderRadius.all(_T.r8),
                  ),
                  child: Text(trend, style: TextStyle(fontSize: 9, fontWeight: FontWeight.w700, color: trendUp ? _T.green : _T.red)),
                ),
              ],
            ),
            const SizedBox(height: 6),
            Text('$value', style: const TextStyle(fontSize: 22, fontWeight: FontWeight.w800, color: _T.ink, height: 1)),
            const SizedBox(height: 1),
            Text(label, style: const TextStyle(fontSize: 10, color: _T.inkLight, fontWeight: FontWeight.w500)),`
);

// ── PATCH 5: Make GridView use horizontal scroll on narrow screens ──
c = c.replace(
`              final cols = constraints.maxWidth < 360 ? 2 : 4;
              return GridView.count(
                shrinkWrap: true,
                physics: const NeverScrollableScrollPhysics(),
                crossAxisCount: cols,
                crossAxisSpacing: 12,
                mainAxisSpacing: 12,
                childAspectRatio: 1.4,`,
`              final isWide = constraints.maxWidth > 600;
              if (isWide) {
                return Row(children: [
                  _statCard(id: 'all',      label: 'Inspections', value: data.total,    icon: Icons.assignment_outlined,   color: const Color(0xFF2D6A2D), trend: '+12%', trendUp: true),
                  const SizedBox(width: 8),
                  _statCard(id: 'disease',  label: 'Disease',     value: data.disease,  icon: Icons.coronavirus_outlined,  color: const Color(0xFFB53030), trend: '+18%', trendUp: false),
                  const SizedBox(width: 8),
                  _statCard(id: 'pest',     label: 'Pests',       value: data.pest,     icon: Icons.bug_report_outlined,   color: const Color(0xFF9A5C00), trend: '-5%',  trendUp: true),
                  const SizedBox(width: 8),
                  _statCard(id: 'critical', label: 'Critical',    value: data.critical, icon: Icons.warning_amber_rounded, color: const Color(0xFF7A1F1F), trend: '+3',   trendUp: false),
                ].map((w) => w is SizedBox ? w : Expanded(child: w)).toList());
              }
              return SizedBox(
                height: 100,
                child: ListView(
                  scrollDirection: Axis.horizontal,
                  children: [
                    SizedBox(width: 130, child: _statCard(id: 'all',      label: 'Inspections', value: data.total,    icon: Icons.assignment_outlined,   color: const Color(0xFF2D6A2D), trend: '+12%', trendUp: true)),
                    const SizedBox(width: 8),
                    SizedBox(width: 130, child: _statCard(id: 'disease',  label: 'Disease',     value: data.disease,  icon: Icons.coronavirus_outlined,  color: const Color(0xFFB53030), trend: '+18%', trendUp: false)),
                    const SizedBox(width: 8),
                    SizedBox(width: 130, child: _statCard(id: 'pest',     label: 'Pests',       value: data.pest,     icon: Icons.bug_report_outlined,   color: const Color(0xFF9A5C00), trend: '-5%',  trendUp: true)),
                    const SizedBox(width: 8),
                    SizedBox(width: 130, child: _statCard(id: 'critical', label: 'Critical',    value: data.critical, icon: Icons.warning_amber_rounded, color: const Color(0xFF7A1F1F), trend: '+3',   trendUp: false)),
                  ],
                ),
              );
              return GridView.count(
                shrinkWrap: true,
                physics: const NeverScrollableScrollPhysics(),
                crossAxisCount: 4,
                crossAxisSpacing: 12,
                mainAxisSpacing: 12,
                childAspectRatio: 1.4,`
);

// ── PATCH 6: Replace AI insight box with gradient card ──
c = c.replace(
"            _aiInsightBox(data),",
`            _buildAiCard(data),`
);

// ── PATCH 7: Add _buildAiCard before _aiInsightBox ──
if (!c.includes('Widget _buildAiCard(')) {
  c = c.replace(
    "  Widget _aiInsightBox(",
    `  Widget _buildAiCard(_PeriodData data) {
    return Container(
      decoration: const BoxDecoration(
        gradient: LinearGradient(colors: [Color(0xFF1B4D1B), Color(0xFF2D6A2D)],
            begin: Alignment.topLeft, end: Alignment.bottomRight),
        borderRadius: BorderRadius.all(Radius.circular(16)),
      ),
      padding: const EdgeInsets.all(14),
      child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
        Row(children: [
          Container(padding: const EdgeInsets.all(5),
            decoration: BoxDecoration(color: Colors.white.withValues(alpha: 0.15), borderRadius: const BorderRadius.all(Radius.circular(8))),
            child: const Icon(Icons.auto_awesome, size: 13, color: Colors.white)),
          const SizedBox(width: 7),
          const Text('AI Insight', style: TextStyle(color: Colors.white, fontWeight: FontWeight.w700, fontSize: 13)),
        ]),
        const SizedBox(height: 8),
        Text(data.aiInsight, style: TextStyle(color: Colors.white.withValues(alpha: 0.9), fontSize: 12, height: 1.4)),
        const SizedBox(height: 8),
        Container(
          padding: const EdgeInsets.all(10),
          decoration: BoxDecoration(color: Colors.white.withValues(alpha: 0.1),
              borderRadius: const BorderRadius.all(Radius.circular(12)),
              border: Border.all(color: Colors.white.withValues(alpha: 0.15))),
          child: Row(crossAxisAlignment: CrossAxisAlignment.start, children: [
            const Icon(Icons.arrow_right_alt, size: 14, color: Colors.white),
            const SizedBox(width: 6),
            Expanded(child: Text(data.aiRecommendation,
                style: TextStyle(color: Colors.white.withValues(alpha: 0.85), fontSize: 11, height: 1.4))),
          ]),
        ),
      ]),
    );
  }

  Widget _aiInsightBox(`
  );
}

// ── PATCH 8: Replace header ──
c = c.replace(
`            // â"€â"€ Header â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€
            const Text(
              'Reports & Analytics',
              style: TextStyle(fontSize: 28, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 4),
            const Text(
              'Inspection trends, findings and performance',
              style: TextStyle(color: Colors.grey, fontSize: 14),
            ),`,
`            Row(children: [
              Expanded(child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                const Text('Reports & Analytics',
                    style: TextStyle(fontSize: 20, fontWeight: FontWeight.w800, color: Color(0xFF1A1F1A), letterSpacing: -0.5)),
                Text('$_selectedFarm · $_selectedDate',
                    style: const TextStyle(fontSize: 11, color: Color(0xFF8A9688), fontWeight: FontWeight.w500)),
              ])),
              _buildHealthBadge(data),
            ]),`
);

// ── PATCH 9: Add _buildHealthBadge method ──
if (!c.includes('Widget _buildHealthBadge(')) {
  c = c.replace(
    "  Widget _buildAiCard(",
    `  Widget _buildHealthBadge(_PeriodData data) {
    final score = ((1 - data.critical / (data.total == 0 ? 1 : data.total)) * 100).clamp(0, 100).round();
    final color = score >= 80 ? const Color(0xFF2D6A2D) : score >= 60 ? const Color(0xFF9A5C00) : const Color(0xFFB53030);
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
      decoration: BoxDecoration(
        color: color.withValues(alpha: 0.1),
        borderRadius: const BorderRadius.all(Radius.circular(12)),
        border: Border.all(color: color.withValues(alpha: 0.3)),
      ),
      child: Column(children: [
        Text('$score', style: TextStyle(fontSize: 22, fontWeight: FontWeight.w900, color: color, height: 1)),
        Text('Health', style: TextStyle(fontSize: 9, color: color, fontWeight: FontWeight.w600, letterSpacing: 0.5)),
      ]),
    );
  }

  Widget _buildAiCard(`
  );
}

// ── PATCH 10: Update inspection list card background ──
c = c.replace(
`      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(18),
      ),
      child: rows.isEmpty`,
`      decoration: const BoxDecoration(
        color: Color(0xFFFFFFFF),
        borderRadius: BorderRadius.all(Radius.circular(16)),
      ),
      child: rows.isEmpty`
);

// ── PATCH 11: Replace top greenhouses container ──
c = c.replace("return Container(\n      decoration: BoxDecoration(\n        color: Colors.white,\n        borderRadius: BorderRadius.circular(18),\n      ),\n      child: Column(\n        children: data.topGreenhouses.asMap",
`return Container(\n      decoration: const BoxDecoration(\n        color: Color(0xFFFFFFFF),\n        borderRadius: BorderRadius.all(Radius.circular(16)),\n      ),\n      child: Column(\n        children: data.topGreenhouses.asMap`
);

const utf8 = require('buffer').Buffer;
fs.writeFileSync(f, c, 'utf8');
console.log('All patches done. Size:', fs.statSync(f).size, 'bytes');
