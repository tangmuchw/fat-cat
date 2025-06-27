const lodash = require("lodash");
const path = require("path");
const fs = require("fs");

const cardTypes = {
    Default: {
        title: "默认",
        subtitle: "-",
        icon: "fa-hands-helping",
        coverTitle: "感谢有你",
        coverSubtitle: "你的帮助温暖我心",
        gradient: "thanks",
        primaryColor: "#ffb88c", // 与首页一致
        darkColor: "#ff8d6b", // 与首页一致
        lightColor: "#fef4eb", // 首页卡片背景色
        textColor: "#8B4513", // 首页深棕色
        secondaryLight: "#fff9f2", // 首页背景渐变色
        secondaryDark: "#ffd6a5",
        contentTitle: "真心感谢你在项目最后阶段帮我修改PPT！",
        contentText:
            "真心感谢你在项目最后阶段帮我修改PPT！你的专业建议让整个展示焕然一新。加班到深夜帮我调整排版和设计，这份付出我铭记于心。PPT最终获得了领导高度评价，这完全归功于你的帮助！",
    },
    Thanks: {
        title: "感谢卡",
        subtitle: "改 PPT 之恩",
        icon: "fa-hands-helping",
        coverTitle: "感谢有你",
        coverSubtitle: "你的帮助温暖我心",
        gradient: "thanks",
        primaryColor: "#FF8E3C",
        darkColor: "#D96527",
        lightColor: "#FFB56B",
        textColor: "#5a3a1e",
        secondaryLight: "#FFD6A5",
        secondaryDark: "#FFB56B",
        contentTitle: "真心感谢你在项目最后阶段帮我修改PPT！",
        contentText:
            "真心感谢你在项目最后阶段帮我修改PPT！你的专业建议让整个展示焕然一新。加班到深夜帮我调整排版和设计，这份付出我铭记于心。PPT最终获得了领导高度评价，这完全归功于你的帮助！",
    },
    Encourage: {
        title: "鼓励卡",
        subtitle: "你是最棒的",
        icon: "fa-trophy",
        coverTitle: "加油向前",
        coverSubtitle: "相信你能做到最好",
        gradient: "encourage",
        primaryColor: "#4facfe",
        darkColor: "#3a8bc7",
        lightColor: "#00c5f2", // 更亮的青色
        textColor: "#1a3d5c",
        secondaryLight: "#9cd9fc",
        secondaryDark: "#4facfe",
        contentTitle: "我相信你的能力，继续加油！",
        contentText:
            "看到你最近为项目付出的努力，我真的很感动。你的坚持和专注是成功的关键，即使遇到困难也从未放弃。请记住，每一次挑战都是成长的机会，我坚信你能突破自我，取得更大的成就！",
    },
    Praise: {
        title: "夸夸卡",
        subtitle: "闪耀的你",
        icon: "fa-star",
        coverTitle: "你真优秀",
        coverSubtitle: "你的光芒无法忽视",
        gradient: "praise",
        primaryColor: "#ff9a9e",
        darkColor: "#d97b7e",
        lightColor: "#fad0c4",
        textColor: "#6b3a3d",
        secondaryLight: "#ffd0d1",
        secondaryDark: "#ff9a9e",
        contentTitle: "你真是太棒了！",
        contentText:
            "今天的演讲实在太精彩了！你的表达清晰流畅，逻辑严谨，台风稳健大方。更难得的是你那份从容不迫的气质，让整个会场都为之折服。这样的表现力，绝对是团队中的佼佼者！",
    },
    Sorry: {
        title: "道歉卡",
        subtitle: "真诚的歉意",
        icon: "fa-dove",
        coverTitle: "深感抱歉",
        coverSubtitle: "希望你能原谅我",
        gradient: "apology",
        primaryColor: "#a18cd1",
        darkColor: "#7c6ca1",
        lightColor: "#fbc2eb",
        textColor: "#4a3f6e",
        secondaryLight: "#c7b9e7",
        secondaryDark: "#a18cd1",
        contentTitle: "真诚地向你道歉",
        contentText:
            "对于昨天的会议迟到，我感到非常抱歉。我的疏忽打乱了大家的计划，浪费了宝贵的时间。这完全是我的责任，没有任何借口。我会更加注意时间管理，确保不再发生类似情况。",
    },
    Reject: {
        title: "拒绝卡",
        subtitle: "委婉的表达",
        icon: "fa-hand-paper",
        coverTitle: "感谢理解",
        coverSubtitle: "下次一定帮忙",
        gradient: "refuse",
        primaryColor: "#ff5858",
        darkColor: "#d14343",
        lightColor: "#f09819",
        textColor: "#6b2a2a",
        secondaryLight: "#ff9d9d",
        secondaryDark: "#ff5858",
        contentTitle: "感谢你的邀请",
        contentText:
            "很感谢你邀请我参加这次活动，能收到你的邀请让我感到非常荣幸。由于近期工作安排紧张，我不得不婉拒这次机会。希望下次有更合适的时间，我一定积极参与。",
    },
    Souvenir: {
        title: "纪念卡",
        subtitle: "美好时光",
        icon: "fa-camera-retro",
        coverTitle: "难忘时刻",
        coverSubtitle: "珍藏这份回忆",
        gradient: "memory",
        primaryColor: "#ffd26f",
        darkColor: "#d9ad56",
        lightColor: "#ff7b54",
        textColor: "#6b4a1e",
        secondaryLight: "#ffe5b1",
        secondaryDark: "#ffd26f",
        contentTitle: "难忘我们共同经历的时光",
        contentText:
            "还记得去年团队建设时我们一起爬山的情景吗？那天的阳光、山风和我们的欢声笑语都深深印在我的记忆里。感谢你在我体力不支时伸出的援手，这份情谊我会永远珍惜。",
    },
    SelfMockery: {
        title: "自嘲卡",
        subtitle: "轻松一笑",
        icon: "fa-theater-masks",
        coverTitle: "自我调侃",
        coverSubtitle: "生活需要幽默感",
        gradient: "self-deprecating",
        primaryColor: "#6a85b6",
        darkColor: "#556a93",
        lightColor: "#bac8e0",
        textColor: "#3a4764",
        secondaryLight: "#a7b7d8",
        secondaryDark: "#6a85b6",
        contentTitle: "又犯了个低级错误，哈哈！",
        contentText:
            "今天居然把咖啡洒在键盘上，还差点把重要文件删除了！我这笨手笨脚的样子真是没救了。不过没关系，我已经学会了自我解嘲，生活嘛，总要有点小插曲才有趣。",
    },
    Embrace: {
        title: "抱抱卡",
        subtitle: "温暖的拥抱",
        icon: "fa-hands",
        coverTitle: "给你抱抱",
        coverSubtitle: "一切都会好起来",
        gradient: "hug",
        primaryColor: "#ff5858",
        darkColor: "#d14343",
        lightColor: "#ffc8c8",
        textColor: "#6b2a2a",
        secondaryLight: "#ffc8c8",
        secondaryDark: "#ff5858",
        contentTitle: "给你一个大大的拥抱",
        contentText:
            "知道你最近压力很大，很想给你一个温暖的拥抱。生活中的困难都是暂时的，你有足够的力量去克服它们。记住，你并不孤单，我们都在你身边支持着你。",
    },
    Recharge: {
        title: "充能卡",
        subtitle: "能量满满",
        icon: "fa-bolt",
        coverTitle: "能量补充",
        coverSubtitle: "满血复活再出发",
        gradient: "energy",
        primaryColor: "#0fd850",
        darkColor: "#0cac41",
        lightColor: "#f9f047",
        textColor: "#1e5c2c",
        secondaryLight: "#a7f09d",
        secondaryDark: "#0fd850",
        contentTitle: "为你补充满满能量！",
        contentText:
            "知道你最近连续加班很辛苦，这张充能卡希望能为你注入新的活力！记得照顾好自己，适当休息才能保持最佳状态。你已经做得很棒了，继续加油！",
    },
    Efficiency: {
        title: "轻效卡",
        subtitle: "轻松高效",
        icon: "fa-feather",
        coverTitle: "轻装上阵",
        coverSubtitle: "高效轻松完成任务",
        gradient: "light",
        primaryColor: "#8e2de2",
        darkColor: "#6e1cb0",
        lightColor: "#aa6aff", // 更明亮的紫色
        textColor: "#3c1a6e",
        secondaryLight: "#b189e6",
        secondaryDark: "#8e2de2",
        contentTitle: "轻松高效完成任务",
        contentText:
            "这个任务看似复杂，其实可以拆分成几个小步骤轻松完成。试试番茄工作法：专注25分钟，休息5分钟。你会发现，高效工作也可以很轻松！",
    },
    Task: {
        title: "任务卡",
        subtitle: "协作完成",
        icon: "fa-tasks",
        coverTitle: "任务协作",
        coverSubtitle: "一起完成这个项目",
        gradient: "task",
        primaryColor: "#11998e",
        darkColor: "#0c736a",
        lightColor: "#4aef9d", // 更亮的绿色
        textColor: "#0c4a42",
        secondaryLight: "#5de0b0",
        secondaryDark: "#11998e",
        contentTitle: "一起完成这个重要任务吧！",
        contentText:
            "市场分析报告需要在本周五前完成，我知道你在这个领域有独到见解。期待你提供的数据分析和市场趋势预测部分，这将对我们决策至关重要！",
    },
    Learning: {
        title: "学习卡",
        subtitle: "共同进步",
        icon: "fa-graduation-cap",
        coverTitle: "学无止境",
        coverSubtitle: "一起探索知识的海洋",
        gradient: "learning",
        primaryColor: "#0b4b7c", // 深蓝色
        darkColor: "#083054", // 更深的蓝色
        lightColor: "#1c9bef", // 天蓝色
        textColor: "#1c3e5c",
        secondaryLight: "#a8d1ff",
        secondaryDark: "#0b4b7c",
        contentTitle: "一起学习新技能吧！",
        contentText:
            "发现了一个很棒的数据分析在线课程，特别适合我们目前的工作需求。要不要一起报名学习？我们可以互相督促，每周讨论学习心得，共同进步！",
    },
    Healing: {
        title: "疗愈卡",
        subtitle: "心灵的抚慰",
        icon: "fa-spa",
        coverTitle: "心灵疗愈",
        coverSubtitle: "让疲惫的心得到休息",
        gradient: "healing",
        primaryColor: "#9d50bb", // 粉紫色
        darkColor: "#7d3f99", // 深紫色
        lightColor: "#6e48aa", // 紫罗兰色
        textColor: "#4a2c5f",
        secondaryLight: "#d3b1e0",
        secondaryDark: "#9d50bb",
        contentTitle: "给自己一些疗愈时光",
        contentText:
            "忙碌的生活中别忘了照顾自己的心灵。推荐你试试冥想APP，每天只需10分钟就能让心灵得到休息。周末要不要一起去公园散步？大自然是最好的疗愈师。",
    },
    Suggestion: {
        title: "建议卡",
        subtitle: "真诚的建议",
        icon: "fa-lightbulb",
        coverTitle: "小小建议",
        coverSubtitle: "希望对你有所帮助",
        gradient: "suggestion",
        primaryColor: "#d66d75",
        darkColor: "#b04a52",
        lightColor: "#f7b5a6", // 珊瑚色
        textColor: "#6b2a2f",
        secondaryLight: "#f0b9bc",
        secondaryDark: "#d66d75",
        contentTitle: "关于项目的一些小建议",
        contentText:
            "非常欣赏你在项目中的创新思维！关于用户界面部分，我有个小建议：简化导航层级可能会提升用户体验。另外，主色调可以考虑更温暖一些，让用户感觉更亲切。",
    },
};

// 将十六进制颜色转换为RGB格式
function hexToRgb(hex) {
    // 移除#号
    hex = hex.replace("#", "");

    // 解析RGB值
    const r = parseInt(hex.substring(0, 2), 16);
    const g = parseInt(hex.substring(2, 4), 16);
    const b = parseInt(hex.substring(4, 6), 16);

    return `${r}, ${g}, ${b}`;
}

const d = Object.entries(cardTypes).reduce((a, [k, colors]) => {
    const primaryColorRgb = hexToRgb(colors.primaryColor);
    const darkColorRgb = hexToRgb(colors.darkColor);
    const secondaryLightRgb = hexToRgb(colors.secondaryLight);
    const secondaryDarkRgb = hexToRgb(colors.secondaryDark);
    const textColorRgb = hexToRgb(colors.textColor);

    const c = {
        ...lodash.pick(colors, [
            "primaryColor",
            "darkColor",
            "lightColor",
            "textColor",
            "secondaryLight",
            "secondaryDark",
        ]),
        primaryColorRgb,
        darkColorRgb,
        secondaryLightRgb,
        secondaryDarkRgb,
        textColorRgb,
    };

    const e = Object.entries(c).reduce((s, [m, n]) => {
        const b = m.replace(/[A-Z]/g, (match, p) => "-" + match.toLowerCase());
        return {
            ...s,
            [b]: n,
        };
    }, {});

    return {
        ...a,
        // [k]: {
        //     ...lodash.pick(colors, ["coverTitle", "coverSubtitle"]),
        // },
        [`card-type-theme-${k}`]: e,
    };
}, {});

const generateLessCode = (themes) => {
    let lessCode = "";

    for (const [themeName, variables] of Object.entries(themes)) {
        // 提取主题名称（去掉前缀）
        const cleanThemeName = themeName.replace("card-type-theme-", "");

        lessCode += `// ${cleanThemeName} 主题\n`;
        lessCode += `@${themeName}: {\n`;

        // 添加所有变量
        for (const [varName, varValue] of Object.entries(variables)) {
            lessCode += `  ${varName}: ${varValue};\n`;
        }

        lessCode += "}\n\n";
    }

    return lessCode;
};

try {
    // console.log("=== lessCode ===");
    const lessContent = generateLessCode(d);
    const fileName = `card_type_themes.less`;
    const filePath = path.join(__dirname, fileName);
    // console.log("d", d);
    const writeStream = fs.createWriteStream(filePath);
    writeStream.write(lessContent);
    writeStream.end();
    console.log(lessContent);
} catch (err) {
    console.error(err);
}
