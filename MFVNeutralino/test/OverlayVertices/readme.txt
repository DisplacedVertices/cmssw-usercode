OverlayTracks: run on all pairs (a,b) of one-vertex events. Take
vertex tracks from event b (stored in minitrees) and add them to
vertex or seed tracks (i.e. those that ended up in the vertex + extra)
from event a (stored in edm files), run the vertexer, and plot whether
two vertices survived as a function of dvv.

Since we vertex in 3D, there are a few models for moving vertex b
tracks in z. There's also the idea to rotate the tracks in x or p
space but it doesn't seem to work yet.

Also only works on MC so far--have to understand how to move for the
beamspot first, maybe we don't care?


Workflow: "run" below means "read, edit+update as needed, test
locally, submit, babysit, gather jobs".

- Produce minitrees as usual (having 3,4,5+-track, and at least 1
  vertex). Put the hadded minitrees on eos somewhere (with appropriate
  sums of qcd or data), the path for which will need to be put in
  several steps below.

- Run makelist.py to make eventlists and jsons for each sample. It
  takes minitrees as input (edit the path at the top of the file
  pointing to the latest trees) and makes lists of run,lumi,event that
  have ntracks=3 or more and nvertex=1 or more. This dumps a lot of
  files in the current dir that skimpick (next step) will read.
  
  It also prints out a thing that you paste into submit.py to inform
  the job splitting.

- Run skimpick.py to make a skim + slim (only keeping beamspot and
  tracks that pass our selection) toward making small files for
  shipping around for jobs. Be sure SkimmedTracks implements the
  latest full track selection.

  It's a very sparse skim so you may want to adjust the
  splitting. It's by file, trying to get about 100 events in each
  output job but with a maximum number of files opened per job
  (problems scale with the latter). There's a little zsh (bash?)
  script at the end of skimpick to help figure out the splitting.

  Be paranoid that you get the right number of events in the end,
  set_events_to_process didn't work at some point.

- While that's running, run prescales.cc/exe (there's a
  Makefile). Only edit the stuff at the top of main(), not the globals
  at the top. This gives prescales.root that you put in the same place
  on eos as minitrees.

- When skimpick is done, "publish" the files with

    mpublish crabdir --dataset pick1vtxvwhatever --include-condor-nevents

  to get some lines for SampleFiles/Samples, along with nevents to
  confirm you got the right amount.

  Then run a merge job on them to get one file per sample with

    python skimpick.py submitmerge

  (edit for the right dataset first/etc.) Put those outputs in another
  dir on eos with one file per sample named like ttbar.root. Replace
  the SampleFiles lines with just pointers to these merged files, and
  you can delete the originals.

- You'll need to do a couple manual merges of the sum samples:
  e.g. qcdht1000sum, JetHT2016BCD, etc. You can do this with
  utilities.py (merge_data and merge_qcd_sum commands).

- Update and run overlay.py. Print the help msg with

    py overlay.py +h

  (Using + instead of - is to avoid conflicting with cmsRun
  argparsing.) A good test is

    cmsRun overlay.py +debug-timing +e 0

  If you do +no-rest-of-event you might not see vertexing events if
  the input file only has a few events and they don't jibe with the
  order in the minitree, and so you won't have tested anything.
  +debug instead of +debug-timing will print waaaay more.

- Submit jobs with submit.py. Uses a modified crab workflow to use
  random cores around the world without requirements on data location,
  since the jobs xrdcp the input files.

JMTBAD finish re assembling output and producing efficiency curves.
