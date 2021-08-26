window.addEventListener("load", function(){
    var noQuery = this.document.getElementById("no-query");
    var queryForm = this.document.getElementById("queries-form");
    var question = this.document.getElementById("question");
    var queriesContainer = this.document.getElementById("queries-container");
    var queryError = this.document.getElementById("query_error");
    
    var answerForm = this.document.getElementById("answer-form");
    var answer = this.document.getElementById("answer");
    var answeringToText =this.document.getElementById("answering-to-text");
    var answerItElems = this.document.querySelectorAll(".answer-it");

    var deleteQueriesElems = this.document.querySelectorAll(".delete-query");
    var deleteAnswerElems = this.document.querySelectorAll(".delete-answer");

    query_id =  null;
    product_id = null;
    questionText = null;

    var onQuerySuccess = function(response) {
        hideBigLoader();

        try {
            var data = JSON.parse(response);

            queryError.innerHTML = "";
            if(data.hasOwnProperty("error")){
                queryError.innerHTML = data.error;
            } 
            else if(data.hasOwnProperty("data")) {
                var obj = data.data;
                if(noQuery) noQuery.remove();
                var addedRow = "<div class='each-query' data-query-id='"+obj.QUERY_ID+"'><div class='query-wrapper'><div class='query-indicator'></div><div><div class='query-text'>"+obj.QUESTION+"</div><div class='querer-detail'><span>by "+obj.QUESTION_BY+"</span><span class='stock-text'>"+obj.AGO_QUESTION+"</span></div><div class='delete-item delete-query' data-query-id='"+obj.QUERY_ID+"' data-product-id="+obj.PRODUCT_ID+"><span>Delete</span></div></div></div></div>";
                queriesContainer.insertAdjacentHTML("afterbegin", addedRow);
                queryForm.reset();
                deleteQueriesElems = document.querySelectorAll(".delete-query");
                resetDeleteQuery();
            }
        } catch (error) {
            window.location.reload();
        }
    }

    if(queryForm){
        queryForm.onsubmit = function(e) {
            e.preventDefault();
            showBigLoader();
    
            var action = queryForm.getAttribute("action");
            var data = new FormData();
            data.append("question", question.value);
            ajax("POST", action, data, onQuerySuccess);
        }
    }

    if(answerItElems){
        answerItElems.forEach(function(item){
            item.onclick = function(){
                var ques = item.parentNode.childNodes[0].nextSibling.innerHTML;
                query_id = item.getAttribute("data-query-id");
                product_id = item.getAttribute("data-product-id");

                ques = ques.substring(0, 50) + (ques.length > 50 ? "..." : "");

                answeringToText.innerHTML = "Answering the query, \""+ques+"\":";
                answerForm.classList.remove("d-none");
                answer.focus();

                questionText = ques;

                answerForm.scrollIntoView({
                    behavior: 'smooth',
                    block: 'center',
                    inline: 'center'
                });
            }
        });
    }

    var onAnswerSuccess = function(response) {
        hideBigLoader();

        try {
            var data = JSON.parse(response);

            queryError.innerHTML = "";
            if(data.hasOwnProperty("error")){
                queryError.innerHTML = data.error;
            } 
            else if(data.hasOwnProperty("data")) {
                var obj = data.data;
                var answerRow = "<div class='query-wrapper answer-wrapper'><div class='query-indicator answer'></div><div><div class='query-text'>"+obj.ANSWER+"</div><div class='querer-detail'><span>by trader</span><span class='stock-text'> "+obj.AGO_ANSWER+"</span></div><div class='delete-item delete-answer' data-query-id='"+obj.QUERY_ID+"' data-product-id="+obj.PRODUCT_ID+"><span>Delete</span></div></div></div></div>";
                var eachRow = document.querySelector(".each-query[data-query-id='"+query_id+"']");
                eachRow.innerHTML += answerRow;
                answerForm.reset();
                answeringToText.innerHTML = "";
                answerForm.classList.add("d-none");
                deleteAnswerElems = document.querySelectorAll(".delete-answer");
                resetDeleteAnswer();

                eachRow.scrollIntoView({
                    behavior: 'smooth',
                    block: 'center',
                    inline: 'center'
                });
            }
        } catch (error) {
            window.location.reload();
        }
    }

    if(answerForm){
        answerForm.onsubmit = function(e) {
            e.preventDefault();
            showBigLoader();

            var action = "/ajax/products/"+product_id+"/add-answer/"+query_id+"/";
            var data = new FormData();
            data.append("answer", answer.value);
            ajax("POST", action, data, onAnswerSuccess);
        }
    }

    var onDeleteSuccess = function(response) {
        hideBigLoader();
        var eachRow = document.querySelector(".each-query[data-query-id='"+query_id+"']");
        eachRow.style = "opacity: 0.3; transition: opacity 1s; pointer-events: none;";
    }

    var onDeleteAnswerSuccess = function(response) {
        hideBigLoader();
        var ansRow = document.querySelector(".each-query[data-query-id='"+query_id+"'] .answer-wrapper");
        ansRow.style = "opacity: 0.3; transition: opacity 1s; pointer-events: none;";
    }

    var resetDeleteQuery = function() {
        deleteQueriesElems.forEach(function(item){
            item.onclick = function(){
                query_id = item.getAttribute("data-query-id");
                product_id = item.getAttribute("data-product-id");
                
                showBigLoader();

                var action = "/ajax/products/"+product_id+"/delete-query/"+query_id+"/";
                var data = new FormData();
                data.append("value", "value");
                ajax("POST", action, data, onDeleteSuccess);
            }
        });
    }

    var resetDeleteAnswer = function() {
        deleteAnswerElems.forEach(function(item){
            item.onclick = function() {
                query_id = item.getAttribute("data-query-id");
                product_id = item.getAttribute("data-product-id");
                
                showBigLoader();

                var action = "/ajax/products/"+product_id+"/delete-answer/"+query_id+"/";
                var data = new FormData();
                data.append("value", "value");
                ajax("POST", action, data, onDeleteAnswerSuccess);
            }
        });
    }
    resetDeleteQuery();
    resetDeleteAnswer();


    // Check if from notification
    var url_string = this.window.location.href;
    var url = new URL(url_string);
    var notif = url.searchParams.get("is_notif");
    var queryIdUrl = url.searchParams.get("query_id");

    if(notif && queryIdUrl) {
        var eachRow = document.querySelector(".each-query[data-query-id='"+queryIdUrl+"']");

        eachRow.scrollIntoView({
            behavior: 'smooth',
            block: 'center',
            inline: 'center'
        });
        eachRow.style = "animation: focusFade 3s";
    }
});