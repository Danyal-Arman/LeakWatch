import { useEffect, useState } from "react";
import { fetchSecurityReports } from "../api/securityApi";
import SeverityBadge from "./SeverityBadge";
import SeverityChart from "./SeverityChart";

import {
  ShieldAlert,
  Mail,
  AlertTriangle,
  BrainCircuit,
  Gauge,
  Activity,
  Eye,
} from "lucide-react";

export default function Dashboard() {
  const [severity, setSeverity] = useState("all");
  const [search, setSearch] = useState("");
  const [reports, setReports] = useState([]);
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [totalUsers, setTotalUsers] = useState(0);
  const [selectedReport, setSelectedReport] = useState(null);

  const PAGE_SIZE = 14;

  useEffect(() => {
    fetchSecurityReports(page, PAGE_SIZE).then((res) => {
      setReports(res.data || []);
      setTotalPages(res.pages || 1);
      setTotalUsers(res.total || 0);
    });
  }, [page]);

  const filtered = reports.filter((report) => {
    const matchSeverity = severity === "all" || report.meta?.severity === severity;

    const keyword = search.toLowerCase();
    const matchSearch =
      report.name?.toLowerCase().includes(keyword) ||
      report.email?.toLowerCase().includes(keyword);

    return matchSeverity && matchSearch;
  });

  const severityData = ["high", "medium", "low"].map((level) => ({
    name: level,
    count: reports.filter((report) => report.meta?.severity === level).length,
  }));

  const highAlerts = reports.filter((report) => report.meta?.severity === "high").length;
  const alertEmailsSent = reports.filter((report) => report.emailSent).length;
  const aiAnalyzedAccounts = reports.filter((report) => report.ai?.confidence !== undefined).length;

  const avgConfidence =
    reports.length > 0
      ? Math.round(
          reports.reduce((sum, report) => sum + (report.ai?.confidence || 0), 0) /
            reports.length,
        )
      : 0;

  const threatLevel =
    highAlerts > 10 ? "CRITICAL" : highAlerts > 3 ? "ELEVATED" : "SECURE";

  const formatDate = (value) => {
    if (!value) return "N/A";
    try {
      return new Date(value).toLocaleString();
    } catch {
      return value;
    }
  };

  const statusBadge = (status) => {
    if (status === "resolved") {
      return "bg-green-500/20 text-green-300 border-green-500/40";
    }
    return "bg-red-500/20 text-red-300 border-red-500/40";
  };

  const emailBadge = (sent) => {
    if (sent) {
      return "bg-green-500/20 text-green-300 border-green-500/40";
    }
    return "bg-orange-500/20 text-orange-300 border-orange-500/40";
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-slate-900 to-black text-white p-6">
      <div className="flex flex-col gap-3 md:flex-row md:justify-between md:items-center mb-8">
        <div>
          <h1 className="text-4xl font-bold bg-gradient-to-r from-cyan-400 to-blue-500 bg-clip-text text-transparent">
            AI User Credential Monitoring Dashboard
          </h1>

          <p className="text-gray-400 mt-2">
            Rule-Based Detection • Groq AI • Email Alerts • MongoDB
          </p>
        </div>

        <div
          className={`px-4 py-2 rounded-full border ${
            threatLevel === "CRITICAL"
              ? "bg-red-500/20 border-red-500 text-red-300"
              : threatLevel === "ELEVATED"
                ? "bg-yellow-500/20 border-yellow-500 text-yellow-300"
                : "bg-green-500/20 border-green-500 text-green-300"
          }`}
        >
          <Activity className="inline mr-2" size={16} />
          {threatLevel}
        </div>
      </div>

      {highAlerts > 0 && (
        <div className="bg-red-600/20 border border-red-500 p-3 rounded mb-6 flex items-center gap-3 animate-pulse duration-0">
          <AlertTriangle className="text-red-400" />
          <span>{highAlerts} high-risk passwords detected</span>
        </div>
      )}

      <div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-4 mb-6">
        <div className="bg-white/10 backdrop-blur-md p-4 rounded-lg border border-white/20">
          <div className="flex items-center gap-2">
            <ShieldAlert size={18} />
            <p>Total Users Monitored</p>
          </div>
          <h2 className="text-2xl font-bold mt-2">{totalUsers}</h2>
        </div>

        <div className="bg-white/10 backdrop-blur-md p-4 rounded-lg border border-white/20">
          <div className="flex items-center gap-2">
            <AlertTriangle size={18} />
            <p>High Risk Passwords</p>
          </div>
          <h2 className="text-2xl font-bold mt-2 text-red-400">{highAlerts}</h2>
        </div>

        <div className="bg-white/10 backdrop-blur-md p-4 rounded-lg border border-white/20">
          <div className="flex items-center gap-2">
            <Mail size={18} />
            <p>Alert Emails Sent</p>
          </div>
          <h2 className="text-2xl font-bold mt-2">{alertEmailsSent}</h2>
        </div>

        <div className="bg-cyan-500/10 backdrop-blur-md p-4 rounded-lg border border-cyan-500/30">
          <div className="flex items-center gap-2">
            <BrainCircuit size={18} />
            <p>AI Analyzed Accounts</p>
          </div>
          <h2 className="text-2xl font-bold mt-2 text-cyan-400">{aiAnalyzedAccounts}</h2>
        </div>
      </div>

      <div className="grid grid-cols-1 xl:grid-cols-12 gap-6 mb-6">
        <div className="xl:col-span-6 bg-white/10 backdrop-blur-md p-4 rounded-lg border border-white/20">
          <h2 className="mb-4 font-semibold">Severity Distribution</h2>
          <SeverityChart data={severityData} />
        </div>

        <div className="xl:col-span-6 bg-white/10 backdrop-blur-md p-4 rounded-lg border border-white/20">
          <h2 className="mb-4 font-semibold">Latest Security Alerts</h2>
          <div className="space-y-3 max-h-[250px] overflow-y-auto">
            {reports.slice(0, 6).map((report) => (
              <div key={report._id} className="border-b border-gray-700 pb-2">
                <p className="text-sm flex items-center gap-2">
                  <SeverityBadge severity={report.meta?.severity} />
                  <span>{report.name}</span>
                </p>
                <p className="text-xs text-gray-400 mt-1">{report.email}</p>
              </div>
            ))}
          </div>
        </div>
      </div>

      <div className="flex flex-col md:flex-row gap-4 mb-4">
        <input
          type="text"
          placeholder="Search by name or email..."
          className="w-full p-2 rounded bg-gray-800 border border-gray-700"
          onChange={(e) => setSearch(e.target.value)}
        />

        <select
          className="p-2 rounded bg-gray-800 border border-gray-700"
          onChange={(e) => {
            setSeverity(e.target.value);
            setPage(1);
          }}
        >
          <option value="all">All</option>
          <option value="high">High</option>
          <option value="medium">Medium</option>
          <option value="low">Low</option>
        </select>
      </div>

      <div className="bg-white/10 backdrop-blur-md rounded-lg border border-white/20 overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead className="bg-gray-800">
              <tr>
                <th className="p-3 text-left">Name</th>
                <th className="p-3 text-left">Email</th>
                <th className="p-3 text-left">Score</th>
                <th className="p-3 text-left">Severity</th>
                <th className="p-3 text-left">AI Confidence</th>
                <th className="p-3 text-left">Email Sent</th>
                <th className="p-3 text-left">Status</th>
                <th className="p-3 text-left">View</th>
              </tr>
            </thead>

            <tbody>
              {filtered.map((report) => (
                <tr key={report._id} className="border-t border-gray-700 hover:bg-gray-800 transition">
                  <td className="p-3">{report.name}</td>
                  <td className="p-3">{report.email}</td>
                  <td className="p-3">{report.meta?.score}</td>
                  <td className="p-3">
                    <SeverityBadge severity={report.meta?.severity} />
                  </td>
                  <td className="p-3">
                    {report.ai?.confidence ? (
                      <span className="text-cyan-400 font-semibold">
                        {report.ai.confidence}%
                      </span>
                    ) : (
                      "N/A"
                    )}
                  </td>
                  <td className="p-3">
                    <span className={`px-2 py-1 rounded-full border text-xs ${emailBadge(report.emailSent)}`}>
                      {report.emailSent ? "Sent" : "Pending"}
                    </span>
                  </td>
                  <td className="p-3">
                    <span className={`px-2 py-1 rounded-full border text-xs ${statusBadge(report.status)}`}>
                      {report.status ? report.status.charAt(0).toUpperCase() + report.status.slice(1) : "Open"}
                    </span>
                  </td>
                  <td className="p-3">
                    <button
                      className="flex items-center gap-1 text-cyan-400 underline"
                      onClick={() => setSelectedReport(report)}
                    >
                      <Eye size={14} />
                      View
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      <div className="flex justify-between mt-4">
        <button
          disabled={page === 1}
          onClick={() => setPage(page - 1)}
          className="bg-red-600 px-4 py-2 rounded disabled:opacity-50"
        >
          Prev
        </button>

        <span>
          Page {page} of {totalPages}
        </span>

        <button
          disabled={page === totalPages}
          onClick={() => setPage(page + 1)}
          className="bg-cyan-600 px-4 py-2 rounded disabled:opacity-50"
        >
          Next
        </button>
      </div>

      {selectedReport && (
        <div className="fixed inset-0 bg-black/70 flex items-center justify-center z-50 p-4">
          <div className="bg-gray-900 p-6 rounded-lg w-full max-w-2xl border border-gray-700 shadow-2xl">
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-xl font-bold">Credential Monitoring Report</h2>
              <button className="text-gray-400 hover:text-white" onClick={() => setSelectedReport(null)}>
                Close
              </button>
            </div>

            <div className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="rounded-lg bg-white/10 p-3 border border-white/10">
                  <p className="text-sm text-gray-400">Name</p>
                  <p className="font-semibold">{selectedReport.name}</p>
                </div>
                <div className="rounded-lg bg-white/10 p-3 border border-white/10">
                  <p className="text-sm text-gray-400">Email</p>
                  <p className="font-semibold">{selectedReport.email}</p>
                </div>
              </div>

              <div className="rounded-lg bg-white/10 p-4 border border-white/10">
                <div className="flex items-center gap-2 mb-3">
                  <span className="text-sm text-gray-400">Rule Score</span>
                  <span className="text-lg font-semibold text-cyan-400">{selectedReport.meta?.score}</span>
                </div>
                <SeverityBadge severity={selectedReport.meta?.severity} />
              </div>

              <div className="rounded-lg bg-white/10 p-4 border border-white/10">
                <p className="text-sm text-gray-400 mb-2">Rule Flags</p>
                <div className="flex flex-wrap gap-2">
                  {(selectedReport.meta?.flags || []).map((flag, index) => (
                    <span key={index} className="rounded-full border border-cyan-500/30 bg-cyan-500/10 px-3 py-1 text-sm text-cyan-300">
                      {flag}
                    </span>
                  ))}
                </div>
              </div>

              <div className="rounded-lg bg-white/10 p-4 border border-white/10">
                <div className="flex items-center justify-between mb-2">
                  <p className="text-sm text-gray-400">AI Severity</p>
                  <span className="text-sm font-semibold text-cyan-400">{selectedReport.ai?.severity ? selectedReport.ai.severity.charAt(0).toUpperCase() + selectedReport.ai.severity.slice(1) : "N/A"}</span>
                </div>
              </div>

              <div className="rounded-lg bg-white/10 p-4 border border-white/10">
                <div className="flex items-center justify-between mb-2">
                  <p className="text-sm text-gray-400">AI Confidence</p>
                  <span className="text-sm font-semibold text-cyan-400">{selectedReport.ai?.confidence || 0}%</span>
                </div>
                <div className="w-full h-2 rounded-full bg-gray-800 overflow-hidden">
                  <div className="h-full rounded-full bg-gradient-to-r from-cyan-500 to-blue-500" style={{ width: `${selectedReport.ai?.confidence || 0}%` }} />
                </div>
              </div>

              <div className="rounded-lg border border-cyan-500/30 bg-cyan-500/10 p-4">
                <p className="text-sm text-cyan-300 mb-2">AI Reason</p>
                <p className="text-sm text-cyan-100">{selectedReport.ai?.reason || "No additional reasoning provided."}</p>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="rounded-lg bg-white/10 p-3 border border-white/10">
                  <p className="text-sm text-gray-400">Email Sent</p>
                  <span className={`mt-1 inline-block rounded-full border px-2 py-1 text-xs ${emailBadge(selectedReport.emailSent)}`}>
                    {selectedReport.emailSent ? "Sent" : "Pending"}
                  </span>
                </div>
                <div className="rounded-lg bg-white/10 p-3 border border-white/10">
                  <p className="text-sm text-gray-400">Status</p>
                  <span className={`mt-1 inline-block rounded-full border px-2 py-1 text-xs ${statusBadge(selectedReport.status)}`}>
                    {selectedReport.status ? selectedReport.status.charAt(0).toUpperCase() + selectedReport.status.slice(1) : "Open"}
                  </span>
                </div>
              </div>

              <div className="rounded-lg bg-white/10 p-3 border border-white/10">
                <p className="text-sm text-gray-400">Detection Time</p>
                <p className="font-medium">{formatDate(selectedReport.createdAt)}</p>
              </div>
            </div>

            <div className="mt-6 flex justify-end">
              <button className="bg-red-600 px-4 py-2 rounded" onClick={() => setSelectedReport(null)}>
                Close
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
