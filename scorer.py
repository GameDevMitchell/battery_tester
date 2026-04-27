# scorer.py
# Scoring engine for the Battery Performance Tester.
# This module calculates impact scores based on CPU, memory, and battery usage metrics.
# It converts raw system metrics into human-readable impact assessments.

from typing import Dict

# CPU thresholds — average CPU usage that defines impact levels
CPU_LOW_THRESHOLD = 15       # Below 15% average CPU = low impact
CPU_MEDIUM_THRESHOLD = 40    # 15–40% = medium impact
# Above 40% = high impact

# Memory thresholds (in MB)
MEMORY_LOW_THRESHOLD = 200   # Below 200MB = low
MEMORY_MEDIUM_THRESHOLD = 500  # 200–500MB = medium

# Battery drain thresholds (percentage points lost during test)
BATTERY_LOW_THRESHOLD = 0.5   # Less than 0.5% drained = low
BATTERY_MEDIUM_THRESHOLD = 2.0  # 0.5–2% = medium


def calculate_score(summary: Dict) -> Dict:
    """
    Calculate impact scores for CPU, memory, and battery usage.
    
    Args:
        summary: Dictionary containing system metrics from BatteryMonitor.get_summary()
        
    Returns:
        Dictionary containing individual scores, overall score, and recommendation
    """
    # Score CPU usage
    cpu_score = _score_cpu(summary['avg_cpu'])
    
    # Score memory usage
    memory_score = _score_memory(summary['avg_memory_mb'])
    
    # Score battery drain (may be N/A if no battery available)
    battery_score = _score_battery(summary['battery_drain'], summary['battery_start'] is None)
    
    # Calculate overall score based on combination of individual scores
    overall_score = _calculate_overall_score(cpu_score, memory_score, battery_score)
    
    # Generate recommendation based on overall score
    recommendation = _get_recommendation(overall_score)
    
    return {
        'cpu_score': cpu_score,
        'memory_score': memory_score,
        'battery_score': battery_score,
        'overall_score': overall_score,
        'recommendation': recommendation
    }


def _score_cpu(avg_cpu: float) -> str:
    """
    Score CPU usage based on average percentage.
    
    Args:
        avg_cpu: Average CPU usage percentage
        
    Returns:
        "Low", "Medium", or "High" impact level
    """
    if avg_cpu < CPU_LOW_THRESHOLD:
        return "Low"
    elif avg_cpu < CPU_MEDIUM_THRESHOLD:
        return "Medium"
    else:
        return "High"


def _score_memory(avg_memory_mb: float) -> str:
    """
    Score memory usage based on average MB used.
    
    Args:
        avg_memory_mb: Average memory usage in megabytes
        
    Returns:
        "Low", "Medium", or "High" impact level
    """
    if avg_memory_mb < MEMORY_LOW_THRESHOLD:
        return "Low"
    elif avg_memory_mb < MEMORY_MEDIUM_THRESHOLD:
        return "Medium"
    else:
        return "High"


def _score_battery(battery_drain: float, no_battery: bool) -> str:
    """
    Score battery drain based on percentage lost during test.
    
    Args:
        battery_drain: Battery percentage drained during test
        no_battery: True if no battery sensor is available
        
    Returns:
        "Low", "Medium", "High", or "N/A" impact level
    """
    if no_battery:
        return "N/A"
    
    if battery_drain < BATTERY_LOW_THRESHOLD:
        return "Low"
    elif battery_drain < BATTERY_MEDIUM_THRESHOLD:
        return "Medium"
    else:
        return "High"


def _calculate_overall_score(cpu_score: str, memory_score: str, battery_score: str) -> str:
    """
    Calculate overall impact score from individual component scores.
    
    Logic:
    - If all three are Low → overall = "🟢 Low Impact"
    - If any one is High OR two are Medium → overall = "🔴 High Impact"
    - Otherwise → overall = "🟡 Medium Impact"
    
    Args:
        cpu_score: CPU impact level
        memory_score: Memory impact level
        battery_score: Battery impact level
        
    Returns:
        Overall impact score with emoji indicator
    """
    # Count high and medium scores (excluding N/A battery scores)
    high_count = 0
    medium_count = 0
    
    for score in [cpu_score, memory_score, battery_score]:
        if score == "High":
            high_count += 1
        elif score == "Medium":
            medium_count += 1
    
    # Determine overall score
    if high_count > 0 or medium_count >= 2:
        return "🔴 High Impact"
    elif high_count == 0 and medium_count == 0:
        return "🟢 Low Impact"
    else:
        return "🟡 Medium Impact"


def _get_recommendation(overall_score: str) -> str:
    """
    Generate user-friendly recommendation based on overall impact score.
    
    Args:
        overall_score: Overall impact score string
        
    Returns:
        Recommendation string for the user
    """
    if "Low Impact" in overall_score:
        return "This app is battery-friendly. Safe to run in the background."
    elif "High Impact" in overall_score:
        return "This app is a battery drain. Close it when not actively using it."
    else:  # Medium Impact
        return "This app has moderate battery impact. Avoid running alongside other heavy apps."
