
/* ----------------------------------------------------------------------
    FULL VALIDATION
-------------------------------------------------------------------------*/

// 1) =============================== Inputmask (PHONE) =============================================
$(document).ready(function(){
    $(".phone").inputmask( {"onincomplete":function(){
        $(".phone").val("");
        swal("Opsss !", "Telefon raqam kiritilmagan !", "info");
        return false;

    }});
});

// 2) INPUT VALIDATION
function validateFormTalant(){
    const ism = document.getElementById('ism').value;
    const familya = document.getElementById('familya').value;
    const phone = document.getElementById('phone').value;
    const login = document.getElementById('login').value;
    const parol = document.getElementById('parol').value;
    const file = document.getElementById('file').value;
    
    console.log("asddddddddddddddddddd")
    // event.preventDefault()

    if (ism === ""){
        swal('Opsss !', 'Ism kiritilmagan', 'error');
        return false;
    }
    else if (ism === ism.toUpperCase()){
        document.getElementById('ism').value="";
        swal('Opsss !', 'Ism faqat katta harflar bilan yozilmasligi kerak', 'info');
        return false;
    }
    else if (familya === ""){
        swal('Opsss !', 'Familya kiritilmagan', 'error');
        return false;
    }
    else if (phone === ""){
        swal('Opsss !', 'Telefon raqam kiritilmagan', 'error');
        return false;
    }
    else if (login === ""){
        swal('Opsss !', 'Login kiritilmagan', 'error');
        return false;
    }
    else if (parol == ""){
        swal('Opsss !', 'Parol kiritilmagan', 'error');
        return false;
    }
    else if (file == ""){
        swal('Opsss !', 'file kiritilmagan', 'error');
        return false;
    }
    else {
        return true;
    }
}

// 3) Maximum allowed upload size
$(document).ready(function() {
    $("#file").bind('change', function(){
        var a = (this.files[0].size);

        if (a > 2 * 1048576){
            swal('Attention !', 'Maximum allowed size is 2mb.', 'info');
            this.value = "";
        }
    });
});

// ==================================== Select 2 Form =============================================
// $(function () {
//     //Initialize Select2 Elements
//     $('.select2').select2()
//   })

$(".ism").keyup(function(){
    if (!/^[a-zA-Z\' _]*$/.test(this.value)){
        this.value = this.value.split(/[^a-zA-Z\' _]/).join('');
    }
})

$(".familya").keyup(function(){
    if (!/^[a-zA-Z\' _]*$/.test(this.value)){
        this.value = this.value.split(/[^a-zA-Z _]/).join('');
    }
})

// 5) Prevent more than 2 white space insice the input NAME
$('.ism').on('keydown', function(){
    var $this = $(this);
    $(this).val($this.val().replace(/(\s{1,})|[^a-zA-Z0-9_']/g, '').replace(/^\s*/, ''));
});

$('.familya').on('keydown', function(){
    var $this = $(this);
    $(this).val($this.val().replace(/(\s{1,})|[^a-zA-Z0-9_']/g, '').replace(/^\s*/, ''));
});


// 6) Prevent starting with space in all inputs (including textarea)
$("input[type='text'], textarea").on("keypress", function(e){
    if(e.which === 32 && ! this.value.length)
    e.preventDefault();
});

function readURL(input) {
    if (input.files && input.files[0]) {
      var reader = new FileReader();
      reader.onload = function(e) {
        $('.image-preview-image').css('background-image', 'url('+e.target.result +')');
      }
      reader.readAsDataURL(input.files[0]);
    }
  }
  
  $("#imageUpload").change(function() {
    readURL(this);
  });