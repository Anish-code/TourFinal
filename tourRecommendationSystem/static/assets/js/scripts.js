console.log("working Fine");

const monthNames = [
  "Jan",
  "Feb",
  "Mar",
  "April",
  "May",
  "June",
  "July",
  "Aug",
  "Sept",
  "Oct",
  "Nov",
  "Dec",
];

$("#commentForm").submit(function (e) {
  e.preventDefault();
  let dt = new Date();
  let time =
    dt.getDate() + " " + monthNames[dt.getUTCMonth()] + ", " + dt.getFullYear();

  $.ajax({
    data: $(this).serialize(),
    method: $(this).attr("method"),
    url: $(this).attr("action"),
    dataType: "json",
    success: function (response) {
      console.log("comment saVED IN DB");

      if (response.bool == true) {
        $("#review-response").html("Review added Successfully");
        $(".hide-comment-form").hide();

        let _html = '<div class="review-o u-s-m-b-15">';
        _html += '<div class="review-o__info u-s-m-b-8">';

        _html +=
          '<span class="review-o__name">' + response.context.user + "</span>";

        _html += '<span class="review-o__date">' + time + "</span></div>";
        for (let i = 1; i <= response.context.rating; i++) {
          _html += '<i class="fas fa-star text: warnnig"></i>';
        }

        _html += "<span>(4)</span></div>";

        _html +=
          '<p class="review-o__text">' + response.context.review + "</p>";
        _html += "</div>";

        $(".comment-list").prepend(_html);
      }
    },
  });
});
