# Multi-Agent Research System - Test Runner
# PowerShell script for Windows

Write-Host "🧪 Starting Test Suite for Multi-Agent Research System" -ForegroundColor Cyan
Write-Host "=" * 60

# Check for pytest
try {
    python -m pytest --version | Out-Null
} catch {
    Write-Host "❌ pytest not found. Installing..." -ForegroundColor Yellow
    pip install pytest pytest-asyncio pytest-cov
}

# Set environment
$env:TESTING = "true"

# Test categories
$UNIT_TESTS = "tests/test_planner.py tests/test_researcher.py tests/test_analyst.py tests/test_synthesizer.py tests/test_critic.py"
$INTEGRATION_TESTS = "tests/test_integration.py"
$QUALITY_TESTS = "tests/test_quality_metrics.py"
$E2E_TESTS = "tests/test_e2e.py tests/test_edge_cases.py"
$API_TESTS = "tests/test_api.py"

Write-Host ""
Write-Host "📦 1. Unit Tests - Individual Agents" -ForegroundColor Yellow
python -m pytest tests/test_planner.py tests/test_researcher.py tests/test_analyst.py tests/test_synthesizer.py tests/test_critic.py -v --tb=short -m "unit" 2>$null
$UNIT_RESULT = $LASTEXITCODE

Write-Host ""
Write-Host "🔗 2. Integration Tests" -ForegroundColor Yellow
python -m pytest tests/test_integration.py -v --tb=short -m "integration" 2>$null
$INTEGRATION_RESULT = $LASTEXITCODE

Write-Host ""
Write-Host "📊 3. Quality Metrics Tests" -ForegroundColor Yellow
python -m pytest tests/test_quality_metrics.py -v --tb=short 2>$null
$QUALITY_RESULT = $LASTEXITCODE

Write-Host ""
Write-Host "🌐 4. API Tests" -ForegroundColor Yellow
python -m pytest tests/test_api.py -v --tb=short -m "api" 2>$null
$API_RESULT = $LASTEXITCODE

Write-Host ""
Write-Host "=" * 60
Write-Host "📈 TEST RESULTS SUMMARY" -ForegroundColor Cyan
Write-Host "=" * 60

if ($UNIT_RESULT -eq 0) {
    Write-Host "✓ Unit Tests: PASSED" -ForegroundColor Green
} else {
    Write-Host "✗ Unit Tests: FAILED" -ForegroundColor Red
}

if ($INTEGRATION_RESULT -eq 0) {
    Write-Host "✓ Integration Tests: PASSED" -ForegroundColor Green
} else {
    Write-Host "✗ Integration Tests: FAILED" -ForegroundColor Red
}

if ($QUALITY_RESULT -eq 0) {
    Write-Host "✓ Quality Tests: PASSED" -ForegroundColor Green
} else {
    Write-Host "✗ Quality Tests: FAILED" -ForegroundColor Red
}

if ($API_RESULT -eq 0) {
    Write-Host "✓ API Tests: PASSED" -ForegroundColor Green
} else {
    Write-Host "✗ API Tests: FAILED" -ForegroundColor Red
}

Write-Host ""
Write-Host "=" * 60

# Overall result
$ALL_PASSED = ($UNIT_RESULT -eq 0) -and ($INTEGRATION_RESULT -eq 0) -and ($QUALITY_RESULT -eq 0) -and ($API_RESULT -eq 0)

if ($ALL_PASSED) {
    Write-Host "🎉 ALL TESTS PASSED!" -ForegroundColor Green
    exit 0
} else {
    Write-Host "❌ SOME TESTS FAILED" -ForegroundColor Red
    exit 1
}
