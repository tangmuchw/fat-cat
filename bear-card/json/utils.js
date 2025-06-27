const fs = require("fs");
const os = require("os");
const XXH = require("xxhashjs");

/**
 * 生成特征的哈希 requestId
 * @param {Object} params 参数
 * @param {number} [seed=0] 哈希种子
 * @returns {string} 16进制哈希字符串
 */
const generateID = (params, seed = 0) => {
    // 1. 序列化查询参数（按key排序）
    const sortedParams = params
        ? Object.keys(params)
              .sort()
              .map((key) => `${key}=${params[key]}`)
              .join("&")
        : "";

    // 3. 拼接特征字符串
    const rawString = [sortedParams].join("|");

    // 4. 生成 SHA-256 哈希（或其他轻量算法如 xxHash）
    const id = XXH.h64(rawString, seed).toString(16);
    return id;
};

const createDirSync = async (dirPath) => {
    if (!fs.existsSync(dirPath)) {
        fs.mkdirSync(dirPath, { recursive: true });
        console.log(`=== 目录已创建: ${dirPath} ===`);
    } else {
        console.log(`=== 目录已存在: ${dirPath} ===`);
    }
};

const getLocalIP = () => {
    const interfaces = os.networkInterfaces();

    for (let name of Object.keys(interfaces)) {
        for (let iface of interfaces[name]) {
            // 跳过 IPv6 和 内部/回环地址
            if (iface.family === "IPv4" && !iface.internal) {
                return iface.address;
            }
        }
    }

    return "127.0.0.1"; // 默认回环地址
};

const getDevCloudUrl = () => {
    const ip = getLocalIP();
    const host = 9000;

    console.log(`=== 本机 IP：${ip} ===`);

    return `http://${ip}:${host}/cover/`;
};

module.exports = {
    createDirSync,
    getLocalIP,
    getDevCloudUrl,
    generateID,
};
