"""
Report Generator for the Security Analyzer.

This module generates security reports in various formats from analysis findings.
"""

import json
import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional


class ReportGenerator:
    """Generator for security analysis reports."""

    def __init__(self):
        """Initialize the report generator."""
        pass

    def generate_report(
        self,
        analysis_result: Dict[str, Any],
        output_file: Optional[str] = None,
        format: str = "json",
        detailed: bool = False
    ) -> None:
        """
        Generate a security report.

        Args:
            analysis_result: Analysis result dictionary
            output_file: Output file path (optional)
            format: Output format (json, html, txt)
            detailed: Generate detailed report
        """
        if format == "json":
            self._generate_json_report(analysis_result, output_file, detailed)
        elif format == "html":
            self._generate_html_report(analysis_result, output_file, detailed)
        elif format == "txt":
            self._generate_txt_report(analysis_result, output_file, detailed)
        else:
            raise ValueError(f"Unsupported format: {format}")

    def _generate_json_report(
        self,
        analysis_result: Dict[str, Any],
        output_file: Optional[str],
        detailed: bool
    ) -> None:
        """
        Generate JSON report.

        Args:
            analysis_result: Analysis result dictionary
            output_file: Output file path
            detailed: Generate detailed report
        """
        report_data = {
            "report_metadata": {
                "timestamp": datetime.datetime.now().isoformat(),
                "format": "json",
                "analyzer_version": "1.0.0",
                "detailed": detailed
            },
            "analysis_summary": {
                "resources_count": analysis_result.get("resources_count", 0),
                "findings_count": analysis_result.get("findings_count", 0),
                "compliance_score": analysis_result.get("compliance_score", 0),
                "summary": analysis_result.get("summary", {})
            },
            "findings": analysis_result.get("findings", [])
        }

        if detailed:
            report_data["detailed_analysis"] = self._generate_detailed_analysis(analysis_result)

        if output_file:
            with open(output_file, 'w') as f:
                json.dump(report_data, f, indent=2)
        else:
            print(json.dumps(report_data, indent=2))

    def _generate_html_report(
        self,
        analysis_result: Dict[str, Any],
        output_file: Optional[str],
        detailed: bool
    ) -> None:
        """
        Generate HTML report.

        Args:
            analysis_result: Analysis result dictionary
            output_file: Output file path
            detailed: Generate detailed report
        """
        html_content = self._build_html_content(analysis_result, detailed)

        if output_file:
            with open(output_file, 'w') as f:
                f.write(html_content)
        else:
            print(html_content)

    def _generate_txt_report(
        self,
        analysis_result: Dict[str, Any],
        output_file: Optional[str],
        detailed: bool
    ) -> None:
        """
        Generate text report.

        Args:
            analysis_result: Analysis result dictionary
            output_file: Output file path
            detailed: Generate detailed report
        """
        txt_content = self._build_txt_content(analysis_result, detailed)

        if output_file:
            with open(output_file, 'w') as f:
                f.write(txt_content)
        else:
            print(txt_content)

    def format_report(self, analysis_result: Dict[str, Any], format: str = "json") -> str:
        """
        Format report content as string.

        Args:
            analysis_result: Analysis result dictionary
            format: Output format

        Returns:
            Formatted report as string
        """
        if format == "json":
            return json.dumps(analysis_result, indent=2)
        elif format == "html":
            return self._build_html_content(analysis_result, False)
        elif format == "txt":
            return self._build_txt_content(analysis_result, False)
        else:
            return "Unsupported format"

    def _build_html_content(self, analysis_result: Dict[str, Any], detailed: bool) -> str:
        """
        Build HTML report content.

        Args:
            analysis_result: Analysis result dictionary
            detailed: Generate detailed report

        Returns:
            HTML content as string
        """
        summary = analysis_result.get("summary", {})
        findings = analysis_result.get("findings", [])

        # Build HTML using string concatenation to avoid f-string issues with CSS
        html_parts = []
        html_parts.append('<!DOCTYPE html>')
        html_parts.append('<html>')
        html_parts.append('<head>')
        html_parts.append('<title>Security Analysis Report</title>')
        html_parts.append('<style>')
        html_parts.append('body { font-family: Arial, sans-serif; margin: 40px; }')
        html_parts.append('.header { background-color: #f0f0f0; padding: 20px; border-radius: 5px; }')
        html_parts.append('.summary { margin: 20px 0; }')
        html_parts.append('.finding { border: 1px solid #ddd; margin: 10px 0; padding: 15px; border-radius: 5px; }')
        html_parts.append('.severity-critical { border-left: 5px solid #dc3545; }')
        html_parts.append('.severity-high { border-left: 5px solid #fd7e14; }')
        html_parts.append('.severity-medium { border-left: 5px solid #ffc107; }')
        html_parts.append('.severity-low { border-left: 5px solid #28a745; }')
        html_parts.append('.compliance-score { font-size: 24px; font-weight: bold; }')
        html_parts.append('table { width: 100%; border-collapse: collapse; }')
        html_parts.append('th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }')
        html_parts.append('th { background-color: #f2f2f2; }')
        html_parts.append('</style>')
        html_parts.append('</head>')
        html_parts.append('<body>')
        html_parts.append('<div class="header">')
        html_parts.append('<h1>Security Analysis Report</h1>')
        html_parts.append(f'<p><strong>Generated:</strong> {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>')
        html_parts.append(f'<p><strong>Resources Analyzed:</strong> {analysis_result.get("resources_count", 0)}</p>')
        html_parts.append(f'<p><strong>Findings:</strong> {analysis_result.get("findings_count", 0)}</p>')
        html_parts.append(f'<p class="compliance-score">Compliance Score: {analysis_result.get("compliance_score", 0)}%</p>')
        html_parts.append('</div>')

        html_parts.append('<div class="summary">')
        html_parts.append('<h2>Summary by Severity</h2>')
        html_parts.append('<table>')
        html_parts.append('<tr><th>Severity</th><th>Count</th></tr>')
        html_parts.append(f'<tr><td>Critical</td><td>{summary.get("critical_findings", 0)}</td></tr>')
        html_parts.append(f'<tr><td>High</td><td>{summary.get("high_findings", 0)}</td></tr>')
        html_parts.append(f'<tr><td>Medium</td><td>{summary.get("medium_findings", 0)}</td></tr>')
        html_parts.append(f'<tr><td>Low</td><td>{summary.get("low_findings", 0)}</td></tr>')
        html_parts.append('</table>')
        html_parts.append('</div>')

        html_parts.append('<div class="summary">')
        html_parts.append('<h2>Services Analyzed</h2>')
        html_parts.append('<ul>')

        for service in summary.get('services_analyzed', []):
            html_parts.append(f'<li>{service}</li>')

        html_parts.append('</ul>')
        html_parts.append('</div>')

        html_parts.append('<div>')
        html_parts.append('<h2>Findings</h2>')

        for finding in findings:
            severity_class = f"severity-{getattr(finding, 'severity', 'low').lower()}"
            html_parts.append(f'<div class="finding {severity_class}">')
            html_parts.append(f'<h3>{getattr(finding, "resource_type", "")}.{getattr(finding, "resource_name", "")}</h3>')
            html_parts.append(f'<p><strong>Severity:</strong> {getattr(finding, "severity", "")}</p>')
            html_parts.append(f'<p><strong>Control:</strong> {getattr(finding, "control_id", "")}</p>')
            html_parts.append(f'<p><strong>Description:</strong> {getattr(finding, "description", "")}</p>')
            html_parts.append(f'<p><strong>Recommendation:</strong> {getattr(finding, "recommendation", "")}</p>')
            html_parts.append(f'<p><strong>File:</strong> {getattr(finding, "file", "")}:{getattr(finding, "line", 0)}</p>')
            html_parts.append(f'<p><strong>Service:</strong> {getattr(finding, "service", "")}</p>')
            html_parts.append('</div>')

        html_parts.append('</div>')
        html_parts.append('</body>')
        html_parts.append('</html>')

        return '\n'.join(html_parts)

    def _build_txt_content(self, analysis_result: Dict[str, Any], detailed: bool) -> str:
        """
        Build text report content.

        Args:
            analysis_result: Analysis result dictionary
            detailed: Generate detailed report

        Returns:
            Text content as string
        """
        summary = analysis_result.get("summary", {})
        findings = analysis_result.get("findings", [])

        txt = f"""
SECURITY ANALYSIS REPORT
{'='*50}

Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Resources Analyzed: {analysis_result.get('resources_count', 0)}
Findings: {analysis_result.get('findings_count', 0)}
Compliance Score: {analysis_result.get('compliance_score', 0)}%

SUMMARY BY SEVERITY
{'-'*30}
Critical: {summary.get('critical_findings', 0)}
High:     {summary.get('high_findings', 0)}
Medium:   {summary.get('medium_findings', 0)}
Low:      {summary.get('low_findings', 0)}

SERVICES ANALYZED
{'-'*30}
"""

        for service in summary.get('services_analyzed', []):
            txt += f"- {service}\n"

        txt += f"""
FINDINGS
{'-'*30}
"""

        for finding in findings:
            txt += f"""
Resource: {getattr(finding, 'resource_type', '')}.{getattr(finding, 'resource_name', '')}
Severity: {getattr(finding, 'severity', '')}
Control:  {getattr(finding, 'control_id', '')}
Description: {getattr(finding, 'description', '')}
Recommendation: {getattr(finding, 'recommendation', '')}
File: {getattr(finding, 'file', '')}:{getattr(finding, 'line', 0)}
Service: {getattr(finding, 'service', '')}
{'-'*50}
"""

        return txt

    def _generate_detailed_analysis(self, analysis_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate detailed analysis section.

        Args:
            analysis_result: Analysis result dictionary

        Returns:
            Detailed analysis dictionary
        """
        findings = analysis_result.get("findings", [])

        # Group findings by service
        findings_by_service = {}
        for finding in findings:
            service = finding.get('service', 'Unknown')
            if service not in findings_by_service:
                findings_by_service[service] = []
            findings_by_service[service].append(finding)

        # Calculate service-level compliance
        service_compliance = {}
        for service, service_findings in findings_by_service.items():
            total_resources = len([f for f in findings if f.get('service') == service])
            if total_resources > 0:
                compliance = max(0, 100 - (len(service_findings) * 10))
                service_compliance[service] = round(compliance, 1)

        return {
            "findings_by_service": findings_by_service,
            "service_compliance": service_compliance,
            "top_risks": self._get_top_risks(findings),
            "recommendations": self._generate_recommendations(findings)
        }

    def _get_top_risks(self, findings: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Get top risks from findings.

        Args:
            findings: List of findings

        Returns:
            Top risks list
        """
        # Sort by severity and count occurrences
        risk_counts = {}
        for finding in findings:
            key = f"{finding.get('control_id', '')}-{finding.get('severity', '')}"
            if key not in risk_counts:
                risk_counts[key] = {
                    "control_id": finding.get('control_id', ''),
                    "severity": finding.get('severity', ''),
                    "description": finding.get('description', ''),
                    "count": 0
                }
            risk_counts[key]["count"] += 1

        # Sort by count and severity
        sorted_risks = sorted(
            risk_counts.values(),
            key=lambda x: (x["severity"], x["count"]),
            reverse=True
        )

        return sorted_risks[:5]  # Top 5 risks

    def _generate_recommendations(self, findings: List[Dict[str, Any]]) -> List[str]:
        """
        Generate high-level recommendations.

        Args:
            findings: List of findings

        Returns:
            List of recommendations
        """
        recommendations = set()

        for finding in findings:
            severity = finding.get('severity', '')
            service = finding.get('service', '')

            if severity in ['CRITICAL', 'HIGH']:
                if service == 'Key Vault':
                    recommendations.add("Review and strengthen Key Vault security configurations")
                elif service == 'Storage':
                    recommendations.add("Implement encryption and access controls for storage accounts")
                elif service == 'Network Security':
                    recommendations.add("Review and restrict network security group rules")
                elif service == 'Virtual Machine':
                    recommendations.add("Enable encryption and secure VM configurations")

        return list(recommendations)

    def generate_from_findings(
        self,
        findings_file: str,
        output: Optional[str] = None,
        format: str = "json"
    ) -> None:
        """
        Generate report from existing findings file.

        Args:
            findings_file: Path to findings JSON file
            output: Output file path
            format: Output format
        """
        try:
            with open(findings_file, 'r') as f:
                findings_data = json.load(f)

            # Create a minimal analysis result structure
            analysis_result = {
                "resources_count": len(findings_data.get("resources", [])),
                "findings_count": len(findings_data.get("findings", [])),
                "compliance_score": findings_data.get("compliance_score", 0),
                "summary": findings_data.get("summary", {}),
                "findings": findings_data.get("findings", [])
            }

            self.generate_report(analysis_result, output, format)

        except Exception as e:
            print(f"Error reading findings file: {e}")
