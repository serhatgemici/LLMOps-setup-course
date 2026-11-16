import pytest
import requests

if __name__ != "__main__":
    pytest.skip(
        "Security evaluation requires the running Docker Compose stack",
        allow_module_level=True,
    )
print("🔒 AUTOMATED SECURITY EVALUATION")
print("=" * 50)

# Test 1: Fetch metrics
response = requests.get("http://localhost:8000/security-metrics")
metrics = response.json()
overview = metrics["overview"]

print("📊 GLOBAL METRICS:")
print(f"  Total requests: {overview['total_requests']}")
print(f"  Blocked requests: {overview['blocked_requests']}")
print(f"  Block rate: {overview['block_rate_percent']:.1f}%")
print(f"  Requests per minute: {overview['requests_per_minute']:.1f}")

# Test 2: Analyze incidents
incidents_response = requests.get("http://localhost:8000/security-incidents")
incidents_data = incidents_response.json()
incidents = incidents_data["incidents"]

attack_types = {}
for incident in incidents[-20:]:  # Last 20 incidents
    attack_type = incident["type"]
    attack_types[attack_type] = attack_types.get(attack_type, 0) + 1

print("\n🚨 DETECTED ATTACK TYPES:")
for attack_type, count in attack_types.items():
    print(f"  {attack_type}: {count} incidents")

# Test 3: Calculate security score
block_rate = overview["block_rate_percent"]
total_requests = overview["total_requests"]

# Scoring Criteria
if total_requests > 100:  # Sufficient sample
    if block_rate >= 90:
        security_score = "🟢 EXCELLENT"
        production_ready = True
    elif block_rate >= 75:
        security_score = "🟡 CORRECT"
        production_ready = True
    elif block_rate >= 50:
        security_score = "🟠 MEDIUM"
        production_ready = False
    else:
        security_score = "🔴 INSUFFICIENT"
        production_ready = False
else:
    security_score = "⏳ INSUFFICIENT SAMPLE"
    production_ready = False

print("\n🎯 FINAL EVALUATION:")
print(f"  Security score: {security_score}")
print(f"  Production ready: {'✅ YES' if production_ready else '❌ NO'}")

# Test 4: Recommendations
print("\n📋 RECOMMENDATIONS:")
if overview["block_rate_percent"] < 5:
    print("  ⚠️  Low block rate - check detection patterns")
if "malicious_prompt" in attack_types:
    print(
        f"  🛡️  {attack_types['malicious_prompt']} injections detected - patterns effective"
    )
if overview["requests_per_minute"] > 50:
    print("  ⚡ High load - monitor performance")

print("\n💡 IMPROVEMENT POINTS:")
print("  • Add multilingual patterns (French injection partially passed)")
print("  • Consider Lakera Guard Pro for advanced AI detection")
print("  • Implement real-time alerts for critical incidents")
