# i_one
내배캠 4기 Node.js 트랙 2번째 팀 프로젝트
<!DOCTYPE html>
<html>

<head>
    <meta charset="utf-8">
    <title>뉴스피드</title>
</head>

<body>
    <style>
          * { box-sizing: border-box; margin: 0; padding: 0; }
        .header {
            background-color: #5d9f;
            color: #fff;
            border-bottom: 1px solid #2c3863;
            height: 45px;
        }
        .bar1 {
            position: absolute;
            left: 0px;
        }
        .search {
            position: absolute;
            left: 300px;
            right: 300px;
        }
        .searchbar {
            border: 1px solid #2c3863;
            width: 100%;
            border-radius: 5px;
            padding: 6px;
            margin-top: 7px;
        }


        .btn1 {
            position: absolute;
            right: 0px;
        }
        .container {
            background-color: #d7d8dc;

        }
        .tab{
        border-top: 1px solid #cccccc;
        background-color: #fafafa;
        height: 50px;
        text-align: center;
        position:fixed;
        bottom: 0;
        left: 0;
        right: 0;
        }
        .tab1 {
            float: left;
            width: 25%;
        }
        .tab2 {
            float: left;
            width: 25%;
        }
        .tab3 {
            float: left;
            width: 25%;
        }
        .tab4 {
            float: left;
            width: 25%;
        }.feed {
            border-top: 1px solid #c0c0c0;
            border-bottom: 1px solid #c0c0c0;
            margin: 7px 0;
            padding: 12px;
        }
        .date {
            color: #999;
            margin-bottom: 10px;
        }
        .title {
            font-weight: 600;
        }
        .content {
            margin-top: 5px;
        }
        .accessory {
            border-top: 1px solid #eee;
            padding-top:10px;
            margin-top:10px;
            color: #999;
            font-size: 14px;
        }

    </style>
    <div class="header">
        <div class="bar1">상단바</div>
        <div class="search">
            <input type="text" class="searchbar" placeholder="Search">
        </div>
        <div class="btn1">새글작성</div>
    </div>
    <div class="container">
        <div class="feed">
            <a class="title">글 제목</a>
            <h5 class="name">이름</h5>
            <h5 class="date">날짜</h5>
            <p class="content">글 내용</p>
            <div class="accessory"> Like  Comments</div>
            </div>

    </div>
<div class="tab">
        <div class="tab1">1</div>
        <div class="tab2">2</div>
        <div class="tab3">3</div>
        <div class="tab4">4</div>
    </div>
    </body>

</html>
