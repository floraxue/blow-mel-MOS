
html_start = """
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

var hidden_div = document.getElementById('hidden_div');
var filenames = hidden_div.innerHTML;
filenames = filenames.split(',');

var randomSubset = getRandomSubarray(filenames, 10);

var audio_reals = [];
var src_reals = [];
var slider_reals = [];
for (i = 0; i < 10; i++) {
    audio_reals.push(document.getElementById('audio' + i));
    src_reals.push(document.getElementById('srcreal' + i));
    slider_reals.push(document.getElementById('sreal' + i));
}

var base_audio_dir = 'https://floraxue.github.io/blow-mel-MOS/audio_files/';
var expname = src_reals[0].src.split("/");
expname = expname[expname.length - 2];

for (i = 0; i < 10; i++) {
    src_reals[i].src = base_audio_dir + expname + '/' + randomSubset[i];
    slider_reals[i].setAttribute("name", expname + '-' + randomSubset[i]);
    audio_reals[i].load();
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
    <crowd-radio-group id="{divname}">
        <crowd-radio-button id="1" name="{expname}-{fname}.same_sure"       value="1">Same speaker: absolutely sure</crowd-radio-button>
        <crowd-radio-button id="2" name="{expname}-{fname}.same_maybe"      value="2">Same speaker: not sure</crowd-radio-button>
        <crowd-radio-button id="3" name="{expname}-{fname}.different_maybe" value="3">Different speakers: not sure</crowd-radio-button>
        <crowd-radio-button id="4" name="{expname}-{fname}.different_sure"  value="4">Different speakers: absolutely sure</crowd-radio-button>
    </crowd-radio-group>
"""

audio_ctrl = """
    <audio class="audio" name="{expname}-{fname}" controls="">
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



