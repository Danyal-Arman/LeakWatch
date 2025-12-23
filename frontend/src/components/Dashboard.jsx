import { useEffect, useState } from "react";
import { fetchPosts } from "../api/postsApi";
import SeverityBadge from "./SeverityBadge";
import SeverityChart from "./SeverityChart";

export default function Dashboard() {
  const [severity, setSeverity] = useState("all");
  const [search, setSearch] = useState("");
  const [posts, setPosts] = useState([]);
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [totalLeaks, setTotalLeaks] = useState(0);
  const [selectedPost, setSelectedPost] = useState(null);
  const [darkMode, setDarkMode] = useState(true);

  const PAGE_SIZE = 14;

  useEffect(() => {
    fetchPosts(page, PAGE_SIZE).then((res) => {
      setPosts(res.data);
      setTotalPages(res.pages);
      setTotalLeaks(res.total);
    });
  }, [page]);

  const filtered = posts.filter((p) => {
    const matchSeverity =
      severity === "all" || p.meta?.severity === severity;

    const matchSearch =
      p.text?.toLowerCase().includes(search.toLowerCase()) ||
      p.user?.toLowerCase().includes(search.toLowerCase()) ||
      p.platform?.toLowerCase().includes(search.toLowerCase());

    return matchSeverity && matchSearch;
  });

  const severityData = ["high", "medium", "low"].map((level) => ({
    name: level,
    count: posts.filter((p) => p.meta?.severity === level).length,
  }));

  return (
    <div
      className={`min-h-screen p-6 transition-colors duration-300 ${
        darkMode ? "bg-gray-900 text-gray-100" : "bg-gray-100 text-gray-900"
      }`}
    >
      {/* HEADER */}
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold">
          Social Media Monitoring for Data Leaks
        </h1>

        <button
          onClick={() => setDarkMode(!darkMode)}
          className="px-4 py-2 rounded bg-indigo-600 text-white hover:bg-indigo-700 transition"
        >
          {darkMode ? "🌞 Light Mode" : "🌙 Dark Mode"}
        </button>
      </div>

      <div className="grid grid-cols-12 gap-6">
        {/* LEFT PANEL */}
        <div className="col-span-4 space-y-6">
          {/* SUMMARY */}
          <div className="grid grid-cols-2 gap-4">
            <div className={`p-4 rounded shadow ${darkMode ? "bg-gray-800" : "bg-white"}`}>
              <p>Total Leaks</p>
              <h2 className="text-2xl font-bold">{totalLeaks}</h2>
            </div>
            <div className={`p-4 rounded shadow ${darkMode ? "bg-gray-800" : "bg-white"}`}>
              <p>Shown</p>
              <h2 className="text-2xl font-bold">{filtered.length}</h2>
            </div>
          </div>

          {/* CHART */}
          <div className={`p-4 rounded shadow ${darkMode ? "bg-gray-800" : "bg-white"}`}>
            <SeverityChart data={severityData} />
          </div>
        </div>

        {/* RIGHT PANEL */}
        <div className={`col-span-8 p-4 rounded shadow ${darkMode ? "bg-gray-800" : "bg-white"}`}>
          {/* FILTER BAR */}
          <div className="flex gap-4 mb-4">
            <input
              type="text"
              placeholder="Search leaks..."
              className={`w-full p-2 rounded border ${
                darkMode
                  ? "bg-gray-700 border-gray-600 text-white"
                  : "bg-white border-gray-300"
              }`}
              onChange={(e) => setSearch(e.target.value)}
            />

            <select
              className={`p-2 rounded border ${
                darkMode
                  ? "bg-gray-700 border-gray-600 text-white"
                  : "bg-white border-gray-300"
              }`}
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

          {/* TABLE */}
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead className={darkMode ? "bg-gray-700" : "bg-gray-200"}>
                <tr>
                  <th className="p-2">Platform</th>
                  <th className="p-2">User</th>
                  <th className="p-2">Description</th>
                  <th className="p-2">Severity</th>
                  <th className="p-2">Source</th>
                </tr>
              </thead>
              <tbody>
                {filtered.map((post) => (
                  <tr key={post.post_id} className="border-t border-gray-600">
                    <td className="p-2">{post.platform}</td>
                    <td className="p-2">{post.user}</td>
                    <td className="p-2">
                      {post.text.slice(0, 60)}...
                      <button
                        className="ml-2 text-blue-500 underline"
                        onClick={() => setSelectedPost(post)}
                      >
                        View
                      </button>
                    </td>
                    <td className="p-2">
                      <SeverityBadge severity={post.meta?.severity} />
                    </td>
                    <td className="p-2">
                      {post.meta?.urls?.[0] ? (
                        <a
                          href={post.meta.urls[0]}
                          target="_blank"
                          className="text-blue-500"
                        >
                          Link
                        </a>
                      ) : (
                        "N/A"
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {/* PAGINATION */}
          <div className="flex justify-between mt-4">
            <button
              disabled={page === 1}
              onClick={() => setPage(page - 1)}
              className="bg-red-600 text-white px-4 py-2 rounded disabled:opacity-50"
            >
              Prev
            </button>
            <span>
              Page {page} of {totalPages}
            </span>
            <button
              disabled={page === totalPages}
              onClick={() => setPage(page + 1)}
              className="bg-green-600 text-white px-4 py-2 rounded disabled:opacity-50"
            >
              Next
            </button>
          </div>
        </div>
      </div>

      {/* MODAL */}
      {selectedPost && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-gray-900 text-white p-6 rounded-lg w-[600px] max-h-[80vh] overflow-y-auto">
            <h2 className="text-xl font-bold mb-2">Leak Details</h2>
            <p><strong>Platform:</strong> {selectedPost.platform}</p>
            <p><strong>User:</strong> {selectedPost.user}</p>
            <p className="my-2"><strong>Description:</strong><br />{selectedPost.text}</p>

            <button
              className="mt-4 bg-red-600 px-4 py-2 rounded"
              onClick={() => setSelectedPost(null)}
            >
              Close
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
