// Top-K benchmark with std::nth_element and a placeholder for a custom implementation.
// Generates N Gaussian(0,1) samples, times nth_element for top-K, and verifies
// correctness of a user-implemented function against the reference.

#include <algorithm>
#include <chrono>
#include <cstdint>
#include <functional>
#include <iostream>
#include <random>
#include <vector>

namespace {

constexpr int N = 160'000;   // dataset size
constexpr int K = 16'000;    // top-K size
static_assert(K >= 0, "K must be non-negative");
static_assert(K <= N, "K must be <= N");

// Contract for contestants:
// - Reorder v in-place such that the last k elements [v.end()-k, v.end())
//   contain the largest k values from the original data (order inside this
//   range does NOT matter), analogous to using std::nth_element with
//   nth = v.end() - k and default comparator (ascending).
// - The contents outside that range are unspecified.
// - Behavior is undefined if k < 0 or k > v.size().
void my_topk_inplace(std::vector<float>& /*v*/, int /*k*/) {
  // TODO: Implement to match the contract above.
}

} // namespace

int main() {
  std::cout << "N=" << N << ", K=" << K << '\n';

  // 1) Generate Gaussian(0,1) data with std::mt19937
  const uint32_t seed = 42u; // Fixed for reproducibility
  std::mt19937 gen(seed);
  std::normal_distribution<float> dist(0.0f, 1.0f);

  std::vector<float> data;
  data.reserve(N);
  for (int i = 0; i < N; ++i) {
    data.push_back(dist(gen));
  }

  // 2) Reference using std::nth_element, measure time
  std::vector<float> ref = data;
  auto t0 = std::chrono::steady_clock::now();
  auto nth = ref.end() - K; // position so that last K are the largest K
  std::nth_element(ref.begin(), nth, ref.end());
  auto t1 = std::chrono::steady_clock::now();

  auto us = std::chrono::duration_cast<std::chrono::microseconds>(t1 - t0).count();
  std::cout << "std::nth_element time: " << us << " us ("
            << (us / 1000.0) << " ms)" << '\n';

  // Extract and sort reference top-K descending for stable comparison
  std::vector<float> top_ref(nth, ref.end());
  std::sort(top_ref.begin(), top_ref.end(), std::greater<float>());

  // 3) Run placeholder implementation on a fresh copy and verify
  std::vector<float> cand = data;
  auto t2 = std::chrono::steady_clock::now();
  my_topk_inplace(cand, K);
  auto t3 = std::chrono::steady_clock::now();
  auto us_cand = std::chrono::duration_cast<std::chrono::microseconds>(t3 - t2).count();

  bool ok = true;
  if (K > 0) {
    if (static_cast<size_t>(K) > cand.size()) {
      ok = false;
    } else {
      auto nth2 = cand.end() - K;
      std::vector<float> top_cand(nth2, cand.end());
      std::sort(top_cand.begin(), top_cand.end(), std::greater<float>());
      ok = (top_cand.size() == top_ref.size()) && std::equal(top_cand.begin(), top_cand.end(), top_ref.begin());
    }
  }

  if (ok) {
    std::cout << "Verification: PASS" << '\n';
    std::cout << "my_topk_inplace time: " << us_cand << " us (" << (us_cand / 1000.0) << " ms)" << '\n';
  } else {
    std::cout << "Verification: FAIL (placeholder not implemented or incorrect)" << '\n';
  }

  return ok ? 0 : 1;
}
