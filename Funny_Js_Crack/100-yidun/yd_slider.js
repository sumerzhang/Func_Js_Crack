// 关键 js 已删除, 请自行补全

function slider_encrypt(token, trace, width) {
    var new_trace = process_trace(token, trace),
        n_ = b_sample(new_trace, 50),
        r_ = t.eypt(t.xor_encode(token, parseInt(trace[trace.length - 1][0] - trace[0][0] + "px", 10) / width * 100 + ""));
    return {
        d: t.eypt(n_.join(":")),
        m: "",
        p: r_,
        ext: t.eypt(t.xor_encode(token, 1 + "," + new_trace.length))
    }
}

function RandomNum(min, max) {
    return Math.floor(Math.random() * (max - min)) + min + 1
}

function click_encrypt(token, trace, position) {
    var new_position = [];
    var new_trace = process_trace(token, trace),
        n_ = b_sample(new_trace, 50);
    var start_time = RandomNum(2000, 5000);
    for (var i = 0, j = position.length; i < j; i++) {
        var z = start_time + RandomNum(1000, 2000);
        var k = t.xor_encode(token, [position[i][0], position[i][1], z] + "");
        new_position.push(k)
    }
    return {
        d: "",
        m: t.eypt(n_.join(':')),
        p: t.eypt(new_position.join(':')),
        ext: t.eypt(t.xor_encode(token, position.length + "," + n_.length))
    }
}


function sense_encrypt(token, trace, position) {
    var new_trace = process_trace(token, trace);
    return {
        d: "",
        m: t.eypt(b_sample(new_trace, 50).join(':')),
        p: t.eypt(t.xor_encode(token, position)),
        ext: t.eypt(t.xor_encode(token, "1," + trace.length))
    }
}

// console.log(process_trace("8df1e4d682d94d14a4b62a6dda9be30f", [[1, 0, 36], [5, 0, 53], [12, 0, 64], [21, 0, 81], [33, 0, 95], [45, 0, 106], [61, 0, 117], [79, 0, 135], [104, 1, 148], [118, 0, 162], [138, 0, 176], [169, 1, 190], [201, 0, 206], [202, 0, 221], [203, 0, 235], [204, 0, 249], [205, 0, 264], [206, 0, 282], [207, 2, 297], [208, 0, 309], [209, 0, 326], [210, 0, 344], [211, 0, 355], [212, 0, 369], [213, 0, 384], [214, 0, 402], [215, 2, 417], [216, 0, 435], [217, 0, 447], [218, 0, 462], [219, 0, 479], [220, 0, 495], [221, 0, 512], [222, 0, 530], [223, 0, 546], [224, 0, 559], [225, 0, 572], [226, 0, 586], [227, 0, 603], [228, 0, 616], [229, 0, 634], [230, 0, 650], [231, 0, 665], [232, 0, 680]],));
// console.log(click_encrypt(
//     "8df1e4d682d94d14a4b62a6dda9be30f",
//     [[1, 0, 36], [5, 0, 53], [12, 0, 64], [21, 0, 81], [33, 0, 95], [45, 0, 106], [61, 0, 117], [79, 0, 135], [104, 1, 148], [118, 0, 162], [138, 0, 176], [169, 1, 190], [201, 0, 206], [202, 0, 221], [203, 0, 235], [204, 0, 249], [205, 0, 264], [206, 0, 282], [207, 2, 297], [208, 0, 309], [209, 0, 326], [210, 0, 344], [211, 0, 355], [212, 0, 369], [213, 0, 384], [214, 0, 402], [215, 2, 417], [216, 0, 435], [217, 0, 447], [218, 0, 462], [219, 0, 479], [220, 0, 495], [221, 0, 512], [222, 0, 530], [223, 0, 546], [224, 0, 559], [225, 0, 572], [226, 0, 586], [227, 0, 603], [228, 0, 616], [229, 0, 634], [230, 0, 650], [231, 0, 665], [232, 0, 680]],
//     [[213, 62], [48, 84], [147, 40]]
// ));
// console.log(get_cb());

function NN(e) {
    var t = {
        "\\": "-",
        "/": "_",
        "+": "."
    };
    return e.replace(/[\\\/+]/g, function (e) {
        return t[e]
    })
}

function encrypt_validate(validate, fp) {
    return NN(t.eypt(validate + "::" + fp))
}
