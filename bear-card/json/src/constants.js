/**
 * 卡片分类类型
 */
const CARD_CATEGORY_TYPES = [
    // 推荐
    {
        categoryType: "HoneyPocket",
        categoryName: "蜂蜜小口袋 🍯",
    },
    // 职场关系
    {
        categoryType: "ResilienceHive",
        categoryName: "充电协作巢 🤝",
    },
    // 家庭关系
    {
        categoryType: "SimmeringHearth",
        categoryName: "时光慢煮灯 💡",
    },
    // 校园场景
    {
        categoryType: "StarlightAtlas",
        categoryName: "青春星轨图 ✨",
    },
    // 成长里程碑
    {
        categoryType: "CouragePawFolios",
        categoryName: "勇气爪印册 🐾",
    },
    // 情绪支持类
    {
        categoryType: "NeuroBlossom",
        categoryName: "神经调香园 🌸",
        // categoryIntro: "每一步成长都是独特的足迹",
    },
    // 争议处理类
    {
        categoryType: "AmygdalaCourt",
        categoryName: "杏仁核仲裁庭 ⚖️",
    },
];

/**
 * 卡片类型字典
 */
const CARD_TYPES_DICTIONARIES = [
    {
        name: "感谢卡",
        value: "thanks",
    },
    {
        name: "鼓励卡",
        value: "encourage",
    },
    {
        name: "夸夸卡",
        value: "praise",
    },
    {
        name: "道歉卡",
        value: "sorry",
    },
    {
        name: "拒绝卡",
        value: "reject",
    },
    {
        name: "纪念卡",
        value: "souvenir",
    },
    {
        name: "自嘲卡",
        value: "selfMockery",
    },
    {
        name: "抱抱卡",
        value: "embrace",
    },
    {
        name: "充能卡",
        value: "recharge",
    },
    {
        name: "轻效卡",
        value: "efficiency",
    },
    {
        name: "任务卡",
        value: "task",
    },
];

module.exports = {
    CARD_CATEGORY_TYPES,
    CARD_TYPES_DICTIONARIES,
};
