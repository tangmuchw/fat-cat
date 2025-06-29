const { parse } = require("json2csv");
const fs = require("fs");
const { CARD_TYPES_DICTIONARIES, CARD_CATEGORY_TYPES } = require("./constants");

function exportToCSV(data, filename) {
    try {
        // 转换 JSON 为 CSV
        const csv = parse(data, {
            fields: Object.keys(data[0]),
            header: true,
        });

        // 写入文件
        fs.writeFileSync(filename, "\uFEFF" + csv, "utf8"); // BOM 解决中文乱码
        console.log(`CSV 文件已保存: ${filename}`);
    } catch (err) {
        console.error(err);
    }
}

// 使用示例
const data = [
    { ID: 1, Name: "张三", Email: "zhangsan@example.com" },
    { ID: 2, Name: "李四", Email: "lisi@test.org" },
];

exportToCSV(CARD_CATEGORY_TYPES, "card_category.csv");
exportToCSV(CARD_TYPES_DICTIONARIES, "card_types.csv");
