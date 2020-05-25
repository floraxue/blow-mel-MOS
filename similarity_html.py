
html_start = """

<HTMLQuestion xmlns="http://mechanicalturk.amazonaws.com/AWSMechanicalTurkDataSchemas/2011-11-11/HTMLQuestion.xsd">
<HTMLContent><![CDATA[
<!-- YOUR HTML BEGINS -->
<!DOCTYPE html>
<html>
<head>
<meta http-equiv='Content-Type' content='text/html; charset=UTF-8'/>
<script type='text/javascript' src='https://s3.amazonaws.com/mturk-public/externalHIT_v1.js'></script>
</head>
<body>
<!-- You must include this JavaScript file -->
<script src="https://assets.crowd.aws/crowd-html-elements.js"></script>
<style>
.invalid {
    border-style: solid;
    border-color: #FF0000 !important;
    border-radius: 10px;
}
</style>
<!-- For the full list of available Crowd HTML Elements and their input/output documentation,
      please refer to https://docs.aws.amazon.com/sagemaker/latest/dg/sms-ui-template-reference.html -->

<!-- You must include crowd-form so that your task submits answers to MTurk -->
<crowd-form answer-format="flatten-objects">
    <!-- Use the short-instructions section for quick instructions that the Worker
    will see while working on the task. Including some basic examples of
    good and bad answers here can help get good results. You can include
    any HTML here. -->
    <short-instructions>
        <p>
            For each pair of audio samples given, please assess whether you think
            the two samples could have been produced by the same speaker.
            Some of the samples may sound somewhat degraded/distorted.
            Please try to listen beyond the distortion and concentrate on identifying the voice.
            Are the two voices the same or different?
            You have the option to indicate how sure you are of your decision.

            Thank you for participating in this HIT!
        </p>
        <p>
          For examples on how to rate, click on "full instructions".
        </p >
        <p>For better results, wear headphones and work in a quiet environment.</p>

    </short-instructions>

    <!-- Use the full-instructions section for more detailed instructions that the
    Worker can open while working on the task. Including more detailed
    instructions and additional examples of good and bad answers here can
    help get good results. You can include any HTML here. -->
    <full-instructions>
        <p>Listen to these examples to get an idea of how to rate:</p >
        <audio name="sample1" controls="">
            <source src="https://tianrengao.github.io/testMOS/audio_files/instructions/washington_gt.wav" type="audio/mpeg" />
        </audio>
        <audio name="sample2" controls="">
            <source src="https://tianrengao.github.io/testMOS/audio_files/instructions/washington_gt.wav" type="audio/mpeg" />
        </audio>
        <p>These are the same speakers. You should choose "same speaker"</p>
        <audio name="sample3" controls="">
            <source src="https://floraxue.github.io/blow-mel-MOS/audio_files/originals/p225.wav" type="audio/mpeg" />
        </audio>
        <audio name="sample4" controls="">
            <source src="https://floraxue.github.io/blow-mel-MOS/audio_files/originals/p226.wav" type="audio/mpeg" />
        </audio>
        <p>These are different speakers. You should choose "different speaker"</p>
    </full-instructions>


    <div>Please listen carefully to each pair of audio samples, and answer whether you think the two samples could have been produced by the same speaker.</div>
    <div>There are 14 pairs of short audios to rate (no longer than 10 seconds each).</div>
    
    <br  />
    <div>Try to ignore the noise/distortions and only concentrate on identifying the voice.</div>
    <div>Remember to read the instructions on the left hand side, and click on full instructions for examples before start working.</div>
    <div>There are hidden tests for quality assurance purposes.</div>

"""


html_end = """

</crowd-form>
<script language='Javascript'>turkSetAssignmentID();</script>

<script type="text/javascript">

function validateForm() {
    var groups = document.querySelectorAll("crowd-radio-group");
    var isValid = true;
    for (var i = 0; i < groups.length; i++) {
        responseGiven = false;
        var children = groups[i].children;
        for (var j = 0; j < children.length; j++) {
            responseGiven = responseGiven || children[j].checked;
        }
        if (!responseGiven) {
            groups[i].className = "invalid";
            isValid = false;
        }
        else {
            groups[i].className = ""
        }
    }
    return isValid;
}
document.querySelector('crowd-form').onsubmit = function(e ) {
    if (!validateForm()) {
        e.preventDefault();
    }
};
function getRandomSubarray(arr, size) {
    var shuffled = arr.slice(0), i = arr.length, min = i - size, temp, index;
    while (i-- > min) {
        index = Math.floor((i + 1) * Math.random());
        temp = shuffled[index];
        shuffled[index] = shuffled[i];
        shuffled[i] = temp;
    }
    return shuffled.slice(min);
}
console.log('here');

var hidden_real_fn = document.getElementById('hidden_real_fn');
var real_fns = hidden_real_fn.innerHTML;
real_fns = real_fns.split(',');
var hidden_original_fn = document.getElementById('hidden_original_fn');
var original_fns = hidden_original_fn.innerHTML;
original_fns = original_fns.split(',');

var randomSubset = getRandomSubarray(real_fns, 10);

var base_audio_dir = 'https://floraxue.github.io/blow-mel-MOS/audio_files/';
var real0_audiosrc_vc = document.getElementById('real0_audiosrc_vc');
var expname = real0_audiosrc_vc.src.split("/");
expname = expname[expname.length - 2];

for (i = 0; i < 10; i++) {
    var audiosrc_vc = document.getElementById('real' + i + "_audiosrc_vc");
    var audiosrc_t = document.getElementById('real' + i + "_audiosrc_t");
    var radios = document.getElementsByClassName('real' + i + "_radio");
    audiosrc_vc.src = base_audio_dir + expname + '/' + randomSubset[i];
    target_fname = randomSubset[i].split('_')[3];  // p226_04242_to_p363.wav
    audiosrc_t.src = base_audio_dir + 'originals/' + target_fname;
    for (j = 0; j < radios.length; j++) {
        var str = radios[j].getAttribute('name');
        var fname_base = randomSubset[i].split('.')[0];
        var res = str.replace('unknown_vc', fname_base);
        radios[j].setAttribute('name', res);
    }
}

var audio_controls = document.getElementsByClassName('audio');
for (i = 0; i < audio_controls.length; i++) {
    audio_controls[i].load();
}

</script>

</body></html>
<!-- YOUR HTML ENDS -->

]]>
</HTMLContent>
<FrameHeight>600</FrameHeight>
</HTMLQuestion>

"""

q_div = """
    <div id="{divname}">
    <p>Could these two audio samples have been produced by the same speaker?</p>
    {audio_control1}
    {audio_control2}
    <br />
    {radio_control}
    </div>
"""

radio_ctrl = """
    <crowd-radio-group>
        <crowd-radio-button class="{divname}" name="{expname}-{fname}.same_sure"       value="1">Same speaker: absolutely sure</crowd-radio-button>
        <crowd-radio-button class="{divname}" name="{expname}-{fname}.same_maybe"      value="2">Same speaker: not sure</crowd-radio-button>
        <crowd-radio-button class="{divname}" name="{expname}-{fname}.different_maybe" value="3">Different speakers: not sure</crowd-radio-button>
        <crowd-radio-button class="{divname}" name="{expname}-{fname}.different_sure"  value="4">Different speakers: absolutely sure</crowd-radio-button>
    </crowd-radio-group>
"""

audio_ctrl = """
    <audio class="audio" name="{expname}" controls="">
        <source id="{divname}" src="https://floraxue.github.io/blow-mel-MOS/audio_files/{dirname}/{fname}" type="audio/mpeg" />
    </audio>
"""


filenames_div = """
    <div id="hidden_real_fn" style="display: none;">
    {real_fns}
    </div>

    <div id="hidden_original_fn" style="display: none;">
    {original_fns}
    </div>
"""



