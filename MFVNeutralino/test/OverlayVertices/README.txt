OverlayTracks: run on all pairs (A,B) of one-vertex events. Take
vertex tracks from event B--those stored in minitrees--and add them to
vertex or seed tracks, i.e. those that ended up in the vertex + extra
from event A--stored in edm files. Then run the vertexer, and plot
whether two vertices survived as a function of dvv.


Technical pieces other than the scripts described in Workflow below:

- SkimmedTracks: used elsewhere, but this gets run to make small edm
  input files that contain only the beamspot and seed tracks for the
  events we want.

- OverlayVertexTracks: reads all the events+tracks from the minitree
  in ctor, and then per edm event input, produces a new set of tracks
  from the vertices or events B.

  Currently this works on MC only--have to understand how to move for
  the beamspot first, maybe we don't care and just let dvv be what it
  is? Reduces statistics, but we have a lot... Minitrees are beamspot
  subtracted

  Since we vertex in 3D, there are a few models for moving vertex B
  tracks in z: deltapv; to move tracks in z by the difference between
  PV B and A; deltasv, to move tracks from B to same z as the SV in A;
  and deltasvgaus, to do the same but put a little gaussian smearing
  on that. Get the width from MC or data if you dare.

  "rest_of_event" is whether to also take along all seed tracks from
  event B instead of just those from vertex B.

  There's also the idea to rotate the tracks in x or p space but it
  crashed last time I (JMT) tried it. Maybe I didn't get the jacobians
  right...

  Prescales are used to turn down the *billion* pairs that you can
  have at low dvv to not waste cpu time. (Don't know yet if we
  sufficiently integrate over all the track/detector space with those
  billion pairs, though.)

  Doubles for truth about vertex A and B are also put in the event for
  Histos below.

- Vertexer was modified to take a "second track source" so that you
  get all seed tracks from event A and the ones OverlayVertexTracks
  produced. The rest of the vertexing algorithm proceeds normally.

- OverlayVertexHistos uses the output of Vertexer and the truth
  doubles to make h_dvv/d3d denominator for all pairs, and numerator
  for:
  - where Vertexer came back with any two vertices;
  - ditto, but each passes the min ntracks requirement;
  - where Vertexer found two vertices in the same spots within our
    position resolution;
  - ditto, but require the vertices to have the same number of tracks
    as before;
  - ditto, but require the vertices to have at least the same number
    of tracks as before;
  - where Vertexer found two vertices with the same tracks, not just
    by number of tracks.
  I consider the last one the figure of merit.

- Plotting scripts divide the numerator/denominator and extract
  h_efficiency.


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

- Figure out what z-model width you want with deltaz.py.

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
