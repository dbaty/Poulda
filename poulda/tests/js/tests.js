$(document).ready(function () {
    // Test 'time_to_str()'
    test('test_parse_querystring_empty', function() {
        same(time_to_str(0), '0s')
        same(time_to_str(1), '1s')
        same(time_to_str(59), '59s')
        same(time_to_str(60), '1m')
        same(time_to_str(61), '1m 1s')
        same(time_to_str(3599), '59m 59s')
        same(time_to_str(3600), '1h')
        same(time_to_str(3661), '1h 1m 1s')
    });
});