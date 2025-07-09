db.collection("sent_card_records")
    .aggregate()
    .match({})
    .sort({
        createAt: -1,
    })
    // .skip(skipNum)
    // .limit(pageSize)
    .lookup({
        from: "cards",
        localField: "cardId",
        foreignField: "_id",
        as: "cardInfoList",
    })
    .lookup({
        from: "users",
        localField: "recipientOpenid",
        foreignField: "openid",
        as: "recipientInfoList",
    })
    .lookup({
        from: "users",
        localField: "senderOpenid",
        foreignField: "openid",
        as: "senderInfoList",
    })
    .addFields({
        cardInfo: {
            $ifNull: [
                $.arrayElemAt([
                    {
                        $map: {
                            input: "$cardInfoList",
                            as: "v",
                            in: {
                                cardTypeCode: "$$v.typeCode",
                                cardTypeName: "$$v.typeName",
                                cardThemeCode: "$$v.themeCode",
                                cardThemeName: "$$v.themeName",
                                cardContent: "$$v.content",
                                cardCover: "$$v.cover",
                                cardTitle: "$$v.title",
                                cardHonoree: "$$v.honoree",
                            },
                        },
                    },
                    0,
                ]),
                {},
            ],
        },
        recipientInfo: {
            $ifNull: [
                $.arrayElemAt([
                    {
                        $map: {
                            input: "$recipientInfoList",
                            as: "v",
                            in: {
                                nickName: "$$v.nickName",
                                avatarUrl: "$$v.avatarUrl",
                            },
                        },
                    },
                    0,
                ]),
                {},
            ],
        },
        senderInfo: {
            $ifNull: [
                $.arrayElemAt([
                    {
                        $map: {
                            input: "$senderInfoList",
                            as: "v",
                            in: {
                                nickName: "$$v.nickName",
                                avatarUrl: "$$v.avatarUrl",
                            },
                        },
                    },
                    0,
                ]),
                {},
            ],
        },
    })
    .project({
        recipientInfoList: 0,
        senderInfoList: 0,
        cardInfoList: 0,
    })
    .end();
