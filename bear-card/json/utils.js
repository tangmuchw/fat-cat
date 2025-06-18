const fs = require("fs");

const createDirSync = async (dirPath) => {
    if (!fs.existsSync(dirPath)) {
        fs.mkdirSync(dirPath, { recursive: true });
        console.log(`=== 目录已创建: ${dirPath} ===`);
    } else {
        console.log(`=== 目录已存在: ${dirPath} ===`);
    }
};

module.exports = {
    createDirSync,
};
