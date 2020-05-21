

html_start = """
<HTMLQuestion xmlns="http://mechanicalturk.amazonaws.com/AWSMechanicalTurkDataSchemas/2011-11-11/HTMLQuestion.xsd">
<HTMLContent><![CDATA[
<!-- You must include this JavaScript file -->
<script src="https://assets.crowd.aws/crowd-html-elements.js"></script>
<script src="//uniqueturker.myleott.com/lib.js" type="text/javascript"></script>
<script type="text/javascript">
(function(){
    var ut_id = "3180196b63ba5fb0b9bee7feadbdfb7b";
    if (UTWorkerLimitReached(ut_id)) {
        document.getElementById('mturk_form').style.display = 'none';
        document.getElementsByTagName('body')[0].innerHTML = "You have already completed the maximum number of HITs allowed by this requester. Please click 'Return HIT' to avoid any impact on your approval rating.";
    }
})();
</script>


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
          Listen to these computer generated speech and assess the quality
          of the audio based on how close it is to natural speech.
          For samples, click on "full instructions".
        </p >
        <p>Excellent - Completely natural speech - 5</p >
        <p>Good - Mostly natural speech - 4</p >
        <p>Fair - Equally natural and unnatural speech - 3</p >
        <p>Poor - Mostly unnatural speech - 2</p >
        <p>Bad - Completely unnatural speech - 1</p >
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
	    <p>This is a real audio recording. You should give a 5</p>
        <audio name="sample2" controls="">
            <source src="https://tianrengao.github.io/testMOS/audio_files/instructions/score-1-synthesis.wav" type="audio/mpeg" />
        </audio>
        <p>This is noise/artifacts. You should give a 1</p>
    </full-instructions>

    <!--<div>-->
    <!--  <p>What is your name?</p>-->
    <!--  <crowd-input name="username" placeholder="example: Jack" required></crowd-input>-->
    <!--</div>-->

    <div>Please listen carefully and give ratings: (5 - Best, 1 - Worst)</div>

"""

html_end = """

</crowd-form>
]]>

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

// var x = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15];
var randomSubset = getRandomSubarray(filenames, 10);

var src_reals = [];
var slider_reals = [];
for (i = 0; i < 10; i++) {
    src_reals.push(document.getElementById('srcreal' + i));
    slider_reals.push(document.getElementById('sreal' + i));
}

var base_audio_dir = 'https://tianrengao.github.io/testMOS/audio_files/';
var expname = src_reals[0].src.split("/");
expname = expname[expname.length - 2];

for (i = 0; i < 10; i++) {
    src_reals[i].src = base_audio_dir + expname + '/' + randomSubset[i];
    slider_reals[i] =  expname + '-' + randomSubset[i];

}
// audio.load();
</script>

</HTMLContent>
<FrameHeight>600</FrameHeight>
</HTMLQuestion>
"""

test = """
    <div>
    <p>On a scale of 1-5, how natural is this audio?</p>
    <audio name="test" controls="">

        <!-- Your audio file URL will be substituted for the "audio_url" variable when
               you publish a batch with an input file containing multiple audio file URLs -->
        <source src="https://tianrengao.github.io/testMOS/audio_files/tests/{testname}.wav" type="audio/mpeg" />

    </audio>
    <crowd-slider name="{testname}" min="1" max="5" step="1" pin="true" required></crowd-slider>
    </div>

"""

real = """
    <div>
    <p>On a scale of 1-5, how natural is this audio?</p>
    <audio name="test1" controls="">

        <!-- Your audio file URL will be substituted for the "audio_url" variable when
               you publish a batch with an input file containing multiple audio file URLs -->
        <source id={src_id} src="https://tianrengao.github.io/SqueezeWaveDemo/{realexp}/{realname}.wav_synthesis.wav" type="audio/mpeg" />

    </audio>
    <crowd-slider id={slider_id} name="{realexp}-{realname}" min="1" max="5" step="1" pin="true" required></crowd-slider>
    </div>

"""

filenames_div = """
    <div id="hidden_div" style="display: none;">
        {filenames}
    </div>
"""

