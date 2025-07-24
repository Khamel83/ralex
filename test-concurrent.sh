#!/bin/bash
# Test concurrent usage scenarios

echo "🧪 CONCURRENT USAGE TESTING"
echo "=" 50

echo "Testing 3 simultaneous requests..."

# Launch 3 requests in parallel
./yolo-code.sh "fix bug 1" > /tmp/test1.log 2>&1 &
./yolo-code.sh "analyze code 2" > /tmp/test2.log 2>&1 &  
./yolo-code.sh "yolo task 3" > /tmp/test3.log 2>&1 &

# Wait for all to complete
wait

echo "Results:"
echo "Request 1 (fix - cheap):"
grep "🤖\|💰 Cost" /tmp/test1.log
echo ""

echo "Request 2 (analyze - smart):"  
grep "🤖\|💰 Cost" /tmp/test2.log
echo ""

echo "Request 3 (yolo - fast):"
grep "🤖\|💰 Cost" /tmp/test3.log
echo ""

echo "Final budget status:"
./yolo-code.sh --budget

rm -f /tmp/test*.log
echo "✅ Concurrent testing complete!"