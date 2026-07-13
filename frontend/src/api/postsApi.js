export async function fetchPosts(page = 1, limit = 10) {
  const res = await fetch(
    `https://leakwatch.onrender.com/posts?page=${page}&limit=${limit}`
  );
  return await res.json();
}
