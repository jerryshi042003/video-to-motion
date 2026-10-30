import * as T from 'three';
import {OrbitControls} from './vendor/jsm/controls/OrbitControls.js';
import {RoomEnvironment} from './vendor/jsm/RoomEnvironment.js';
import {GLTFLoader} from './vendor/jsm/loaders/GLTFLoader.js';
const $=id=>document.getElementById(id),stage=$('stage');
// Gallery vendoring: data lives in data/, and ?point=<id>&embed=1&camera=<name>&footage=1&autoplay=1 opens one point inside an iframe.
const DATA='data/',params=new URLSearchParams(location.search),EMBED=params.get('embed')==='1',LOOP=EMBED&&params.get('autoplay')==='1';
const CAMERA_ALIASES={behind:'rear',rear:'rear',back:'rear',front:'front',side:'side',top:'top',free:'oblique',oblique:'oblique',grip:'grip',impact:'impact',source:'source'};
if(EMBED){document.documentElement.classList.add('embed');if(params.get('footage')!=='1')document.documentElement.classList.add('no-footage');const sc=$('source-canvas');sc.width=960;sc.height=436;}
const renderer=new T.WebGLRenderer({antialias:true,preserveDrawingBuffer:true});renderer.toneMapping=T.ACESFilmicToneMapping;renderer.toneMappingExposure=.85;renderer.setPixelRatio(Math.min(devicePixelRatio,2));stage.append(renderer.domElement);
const scene=new T.Scene();scene.background=new T.Color('#17241e');
const camera=new T.PerspectiveCamera(42,1,.01,100);camera.position.set(3,2,-4);
const orbit=new OrbitControls(camera,renderer.domElement);orbit.target.set(0,1,0);orbit.update();
scene.add(new T.HemisphereLight(0xe5f3de,0x526151,.7));const light=new T.DirectionalLight(0xffffff,1.4);light.position.set(-3,6,-4);scene.add(light);
const equipmentEnv=new T.PMREMGenerator(renderer);scene.environment=equipmentEnv.fromScene(new RoomEnvironment(),.04).texture;scene.environmentIntensity=.6;
scene.add(new T.GridHelper(20,40,0x71907a,0x294235));
const ball=new T.Mesh(new T.SphereGeometry(.033,24,16),new T.MeshStandardMaterial({color:0xe1f529,roughness:.8}));scene.add(ball);
const impact=new T.Mesh(new T.SphereGeometry(.009,12,8),new T.MeshBasicMaterial({color:0xffb47d}));scene.add(impact);
const normal=new T.ArrowHelper(new T.Vector3(0,0,1),new T.Vector3(),.28,0xffb47d);scene.add(normal);
const racket=new T.Group(),ghostRacket=new T.Group();scene.add(racket,ghostRacket);ghostRacket.visible=false;
const raw=(await new GLTFLoader().loadAsync(DATA+'racket.glb')).scene;
raw.traverse(o=>{if(o.isMesh&&o.material?.name==='grommet_polymer')o.material.envMapIntensity=.10;});
const transform=new T.Matrix4().set(0,1,0,0,0,0,-1,-.08,-1,0,0,0,0,0,0,1);raw.applyMatrix4(transform);racket.add(raw);
const rawGhost=raw.clone(true);rawGhost.traverse(o=>{if(o.isMesh)o.material=new T.MeshBasicMaterial({color:0xec8e75,wireframe:true,transparent:true,opacity:.25,depthWrite:false});});ghostRacket.add(rawGhost);
let framing={center:new T.Vector3(0,.25,0),radius:1.8};
let entry,arrays,body,frame=0,playing=false,previous=performance.now(),mode='new',view='oblique',loadId=0;
const normalMatrix=new T.Matrix4(),temp=new T.Matrix4(),vector=new T.Vector3();
const mats=Array.from({length:52},()=>new T.Matrix4());
function material(){return new T.ShaderMaterial({toneMapped:false,uniforms:{bones:{value:mats},color:{value:new T.Color(0xc5d0c1)}},vertexShader:`attribute vec4 indicesA;attribute vec4 indicesB;attribute vec4 weightsA;attribute vec4 weightsB;uniform mat4 bones[52];varying vec3 vNormal;void main(){mat4 skin=bones[int(indicesA.x)]*weightsA.x+bones[int(indicesA.y)]*weightsA.y+bones[int(indicesA.z)]*weightsA.z+bones[int(indicesA.w)]*weightsA.w+bones[int(indicesB.x)]*weightsB.x+bones[int(indicesB.y)]*weightsB.y+bones[int(indicesB.z)]*weightsB.z+bones[int(indicesB.w)]*weightsB.w;vNormal=normalize(normalMatrix*mat3(skin)*normal);gl_Position=projectionMatrix*modelViewMatrix*skin*vec4(position,1.);}`,fragmentShader:`uniform vec3 color;varying vec3 vNormal;void main(){vec3 n=normalize(vNormal);float l=.45+.5*max(0.,dot(n,normalize(vec3(-.4,.8,-.6))))+.15*max(0.,dot(n,normalize(vec3(.8,.4,.5))));gl_FragColor=vec4(color*l,1.);
#include <tonemapping_fragment>
#include <colorspace_fragment>
}`});}
function at(name,f,dim){return arrays[name].subarray(f*dim,(f+1)*dim);}
function matrix3(a,m=new T.Matrix4()){return m.set(a[0],a[1],a[2],0,a[3],a[4],a[5],0,a[6],a[7],a[8],0,0,0,0,1);}
function sample(tag,f){
  const lo=Math.floor(f),hi=Math.min(entry.frames-1,lo+1),u=f-lo,qs=[],js=[],ms=[];
  const data=arrays[tag+'_quat'],qa=new T.Quaternion(),qb=new T.Quaternion(),delta=new T.Vector3();
  for(let k=0;k<52;k++){
    qa.fromArray(data,lo*208+k*4);qb.fromArray(data,hi*208+k*4);const q=qa.clone().slerp(qb,u);
    const joint=new T.Vector3().fromArray(arrays.rest_joints,k*3);
    if(k===0){const a=new T.Vector3().fromArray(arrays[tag+'_trans'],lo*3),b=new T.Vector3().fromArray(arrays[tag+'_trans'],hi*3);joint.add(a.lerp(b,u));}
    else{const parent=entry.parents[k];delta.fromArray(arrays.rest_joints,k*3).sub(new T.Vector3().fromArray(arrays.rest_joints,parent*3));joint.copy(js[parent]).add(delta.applyQuaternion(qs[parent]));q.premultiply(qs[parent]);}
    qs.push(q);js.push(joint);const m=new T.Matrix4().makeRotationFromQuaternion(q);const t=new T.Vector3().fromArray(arrays.rest_joints,k*3).applyQuaternion(q);m.setPosition(joint.clone().sub(t));ms.push(m);
  }
  return {qs,js,ms};
}
function poseEquipment(group,tag,f,skin){
  const lo=Math.floor(f),hi=Math.min(entry.frames-1,lo+1),u=f-lo,rw=entry.hand==='left'?20:21;
  const q=new T.Quaternion().fromArray(arrays[tag+'_grip_quat'],lo*4).slerp(new T.Quaternion().fromArray(arrays[tag+'_grip_quat'],hi*4),u).premultiply(skin.qs[rw]);
  const offsets=arrays[tag+'_hand_offset'],variable=offsets.length>3;
  const p=new T.Vector3().fromArray(offsets,variable?lo*3:0).lerp(new T.Vector3().fromArray(offsets,variable?hi*3:0),u).applyQuaternion(skin.qs[rw]).add(skin.js[rw]);
  group.matrixAutoUpdate=false;group.matrix.makeRotationFromQuaternion(q);group.matrix.setPosition(p);
}
function wrist(f){return sample(mode,f).js[entry.hand==='left'?20:21].clone();}
function fitClipBounds(){
  const bounds=new T.Box3(),point=new T.Vector3(),root=new T.Vector3(),origin=new T.Vector3(),points=[];
  const include=p=>{bounds.expandByPoint(p);points.push(p.clone());};
  for(const tag of ['old','new'])for(let f=0;f<entry.frames;f++){
    root.fromArray(arrays[tag+'_joints'],f*156);
    for(let j=0;j<52;j++)include(point.fromArray(arrays[tag+'_joints'],f*156+j*3).sub(root));
    const rotation=matrix3(at(tag+'_racket',f,9));origin.fromArray(arrays[tag+'_origin'],f*3);
    for(const x of [-.14,.14])for(const y of [-.08,.63])include(point.set(x,y,0).applyMatrix4(rotation).add(origin).sub(root));
  }
  framing={center:bounds.getCenter(new T.Vector3()),radius:bounds.getSize(new T.Vector3()).length()/2+.18,points};
}
function bodyFocus(f){return new T.Vector3().fromArray(at(mode+'_joints',Math.floor(f),156)).add(framing.center);}

function sourceCrop(f,aspect){
  const video=$('source');
  if($('full-source').checked){const h=Math.max(video.videoHeight,video.videoWidth/aspect),w=h*aspect;return {x:(video.videoWidth-w)/2,y:(video.videoHeight-h)/2,w,h};}
  const j=at('old_joints',f,156),cr=at('CR',Math.floor(f),9),ct=at('CT',Math.floor(f),3),k=arrays.K;
  const points=[];
  for(let i=0;i<22;i++){
    const x=j[i*3],y=j[i*3+1],z=j[i*3+2],cx=cr[0]*x+cr[1]*y+cr[2]*z+ct[0],cy=cr[3]*x+cr[4]*y+cr[5]*z+ct[1],cz=cr[6]*x+cr[7]*y+cr[8]*z+ct[2];
    if(cz>0)points.push([(k[0]*cx+k[2]*cz)/cz,(k[4]*cy+k[5]*cz)/cz]);
  }
  const observed=at('target',f,10),weights=at('weight',f,5);for(let i=0;i<5;i++)if(weights[i]>.1)points.push([observed[i*2],observed[i*2+1]]);
  const xs=points.map(p=>p[0]),ys=points.map(p=>p[1]),height=Math.max(...ys)-Math.min(...ys),cx=(Math.min(...xs)+Math.max(...xs))/2,cy=(Math.min(...ys)+Math.max(...ys))/2;
  let h=Math.min(video.videoHeight,Math.max(height*1.3,450)),w=Math.max(h*aspect,(Math.max(...xs)-Math.min(...xs))*1.2);h=Math.max(h,w*(1/aspect));
  const x=Math.max(0,Math.min(video.videoWidth-w,cx-w/2)),y=Math.max(0,Math.min(video.videoHeight-h,cy-h/2));
  return {x,y,w,h};
}
function paintSource(){
  const video=$('source'),canvas=$('source-canvas'),ctx=canvas.getContext('2d');
  if(!entry||video.readyState<2||!video.videoWidth)return;
  const f=Math.max(0,Math.min(entry.frames-1,Math.floor(video.currentTime*entry.source_fps+1e-5)-entry.source_start));
  const {x,y,w,h}=sourceCrop(f,canvas.width/canvas.height);
  ctx.fillStyle='#08100b';ctx.fillRect(0,0,canvas.width,canvas.height);ctx.drawImage(video,x,y,w,h,0,0,canvas.width,canvas.height);
  ctx.fillStyle='#101912db';ctx.fillRect(0,0,canvas.width,42);ctx.fillStyle='#e1efcb';ctx.font='22px system-ui';ctx.fillText(`Source frame ${entry.source_start+f} · motion frame ${f}`,18,29);canvas.dataset.testid='source-'+entry.id+'-'+f;
}
$('source').addEventListener('seeked',()=>{paintSource();if(entry&&view==='source')updateView(frame);});$('source').addEventListener('loadeddata',()=>{if(entry)$('source').currentTime=(entry.source_start+frame+.001)/entry.source_fps;paintSource();if(entry&&view==='source')updateView(frame);});
function updateView(f){
  if(!entry)return;const root=new T.Vector3().fromArray(at(mode+'_joints',Math.floor(f),156)),w=wrist(f);let target=bodyFocus(f),offset=new T.Vector3(2,1.15,-2.5);
  if(view==='rear')offset.set(0,.65,-2.7);if(view==='top')offset.set(0,2.7,-.02);if(view==='front')offset.set(0,.65,2.7);if(view==='side')offset.set(2.7,.65,0);
  if(view==='grip'){target=w;offset=new T.Vector3(.30,.12,.55).transformDirection(racket.matrix).multiplyScalar(.65);}if(view==='impact'){target=new T.Vector3(0,.432,0).applyMatrix4(racket.matrix);offset=new T.Vector3(.60,.10,.15).transformDirection(racket.matrix).normalize().multiplyScalar(.85);}
  if(view==='source'){
    const cr=at('CR',Math.floor(f),9),ct=at('CT',Math.floor(f),3),cv=matrix3(cr).transpose();vector.set(...ct).applyMatrix4(cv).negate();
    cv.multiply(new T.Matrix4().makeScale(1,-1,-1));camera.position.copy(vector);camera.quaternion.setFromRotationMatrix(cv);
    if($('source').videoWidth){const b=sourceCrop(Math.floor(f),camera.aspect),k=arrays.K,near=camera.near,far=camera.far;camera.projectionMatrix.set(2*k[0]/b.w,0,1-2*(k[2]-b.x)/b.w,0,0,2*k[4]/b.h,2*(k[5]-b.y)/b.h-1,0,0,0,-(far+near)/(far-near),-2*far*near/(far-near),0,0,-1,0);camera.projectionMatrixInverse.copy(camera.projectionMatrix).invert();}
    orbit.enabled=false;return;
  }
  camera.fov=42;camera.updateProjectionMatrix();if(view!=='grip'&&view!=='impact'){const vertical=T.MathUtils.degToRad(camera.fov/2),horizontal=Math.atan(Math.tan(vertical)*camera.aspect);const direction=offset.clone().normalize(),right=new T.Vector3().crossVectors(new T.Vector3(0,1,0),direction).normalize(),up=new T.Vector3().crossVectors(direction,right).normalize();let distance=0;for(const p of framing.points){const q=p.clone().sub(framing.center),depth=q.dot(direction);distance=Math.max(distance,depth+(Math.abs(q.dot(right))+.13)/Math.tan(horizontal),depth+(Math.abs(q.dot(up))+.13)/Math.tan(vertical));}offset.copy(direction).multiplyScalar(distance*1.04);}
  camera.position.copy(target).add(offset);orbit.target.copy(target);orbit.enabled=true;orbit.update();
}
function ballAt(f){
  ball.visible=false;impact.visible=false;normal.visible=false;if(!$('ball').checked)return 'Ball hidden';
  const event=entry.audit.non_contact_events?.find(e=>f>=e.start&&f<=e.end);
  if(event?.ball_hand)return `Ball: held in ${event.ball_hand} hand in footage; 3D ball hidden`;
  for(const b of entry.balls){
    const flight=b.flight;
    if(mode==='new'&&flight&&f>=flight.frames[0]&&f<=flight.frames.at(-1)){
      const dt=f/entry.fps-b.contact_seconds;let v=[...(dt<0?b.incoming_velocity:b.outgoing_velocity)],p=[...b.center_at_contact];const h=dt/80,k=b.assumed_drag_inverse_m||0,acc=v=>{const n=Math.hypot(...v);return v.map((x,i)=>(i===1?-9.81:0)-k*n*x);};for(let i=0;i<80;i++){const a1=acc(v),v2=v.map((x,j)=>x+a1[j]*h/2),a2=acc(v2),v3=v.map((x,j)=>x+a2[j]*h/2),a3=acc(v3),v4=v.map((x,j)=>x+a3[j]*h),a4=acc(v4);p=p.map((x,j)=>x+h*(v[j]+2*v2[j]+2*v3[j]+v4[j])/6);v=v.map((x,j)=>x+h*(a1[j]+2*a2[j]+2*a3[j]+a4[j])/6);}ball.position.set(...p);ball.visible=true;if(Math.abs(dt)<.0001){impact.position.set(...b.string_point);impact.visible=true;}return 'Ball: inferred flight from observed 2D samples';
    }
  }
  const c=entry.audit.contacts.find(c=>c.frame===f);if(!c)return 'Ball: no defensible flight at this frame';
  if(c.impact_unverified)return 'Ball hidden: impact unverified in the source';
  if(mode==='new'&&c.ball_contact_3d){
    ball.position.set(...c.ball_contact_3d.center);impact.position.set(...c.ball_contact_3d.string_point);ball.visible=true;impact.visible=true;
    return 'Ball: observed 2D ray, inferred string-plane depth; flight unavailable';
  }
  const p=new T.Vector3(.0009844,.4320123,0).applyMatrix4(racket.matrix),n=new T.Vector3(0,0,1).transformDirection(racket.matrix);
  // A contact marker has no flight and is never attached across frames.
  impact.position.copy(p);impact.visible=true;normal.position.copy(p);normal.setDirection(n);normal.visible=true;
  return 'Ball hidden: no supported 3D position; orange mark estimates the string-bed contact';
}
function draw(f,seekSource=false){
  if(!entry)return;frame=Math.max(0,Math.min(entry.frames-1,f));const skin=sample(mode,frame);
  for(let i=0;i<52;i++)mats[i].copy(skin.ms[i]);
  poseEquipment(racket,mode,frame,skin);poseEquipment(ghostRacket,'old',frame,sample('old',frame));ghostRacket.visible=$('ghost').checked&&mode==='new';
  const ballText=ballAt(frame);const near=entry.audit.contacts.reduce((best,c)=>!best||Math.abs(c.frame-frame)<Math.abs(best.frame-frame)?c:best,null);
  $('seek').value=frame;if(document.activeElement!==$('frame-number'))$('frame-number').value=frame.toFixed(2);$('readout').textContent=`${frame.toFixed(2)} / ${entry.frames-1} · ${(frame/entry.fps).toFixed(3)} s`;
  const coverage=Array.from(at('weight',Math.round(frame),5)).filter(w=>w>0).length;
  const manual=entry.audit.manual_racket_annotations?.some(a=>a.frame===Math.round(frame));
  const event=entry.audit.non_contact_events?.find(e=>frame>=e.start&&frame<=e.end);
  const phase=event?event.label:!near?'No labelled stroke':Math.abs(frame-near.frame)<=entry.fps*.16?`${near.kind} · contact neighbourhood at ${near.frame}`:frame<near.frame?`Preparation for ${near.kind} at ${near.frame}`:`Recovery after ${near.kind} at ${near.frame}`;
  $('status').textContent=`Motion: ${phase} · ${entry.hand.toUpperCase()} hitting hand\nRacket: rebuilt model · ${mode==='new'?'new motion fit':'previous motion fit'} · grip ${mode==='new'?'inferred per stroke':'previous fixed registration'}\n${ballText}\nRacket source points at nearest frame: ${coverage}/5${manual?' · includes manual anchors':''}${coverage?'':' · orientation interpolated; inspect source'}`;
  if(seekSource)$('source').currentTime=(entry.source_start+frame+.001)/entry.source_fps;
  if(view==='source')updateView(frame);
  else{
    let target=bodyFocus(frame);
    if(view==='grip')target=wrist(frame);if(view==='impact')target=new T.Vector3(0,.432,0).applyMatrix4(racket.matrix);
    camera.position.add(target.clone().sub(orbit.target));orbit.target.copy(target);orbit.update();
  }
  renderer.render(scene,camera);
}
async function load(id){
  const token=++loadId;playing=false;$('source').pause();$('play').textContent='Play';$('error').textContent='';$('status').removeAttribute('data-testid');
  try{
    const e=await(await fetch(DATA+id+'.json')).json(),buffer=await(await fetch(DATA+e.binary)).arrayBuffer();if(token!==loadId)return;
    entry=e;$('clip').value=e.id;arrays={};for(const [name,l]of Object.entries(e.layout))arrays[name]=new Float32Array(buffer,l.offset,l.length);
    if(body){scene.remove(body);body.geometry.dispose();body.material.dispose();}
    const geom=new T.BufferGeometry();geom.setAttribute('position',new T.BufferAttribute(arrays.rest,3));geom.setIndex(new T.BufferAttribute(new Uint16Array(arrays.faces),1));geom.computeVertexNormals();
    const count=arrays.rest.length/3,ia=new Float32Array(count*4),ib=new Float32Array(count*4),wa=new Float32Array(count*4),wb=new Float32Array(count*4);
    for(let v=0;v<count;v++){const influences=[];for(let j=0;j<52;j++)if(arrays.weights[v*52+j]>0)influences.push([j,arrays.weights[v*52+j]]);if(influences.length>8)throw Error('Skin influence truncation');for(let k=0;k<influences.length;k++){(k<4?ia:ib)[v*4+k%4]=influences[k][0];(k<4?wa:wb)[v*4+k%4]=influences[k][1];}}
    for(const [name,a]of Object.entries({indicesA:ia,indicesB:ib,weightsA:wa,weightsB:wb}))geom.setAttribute(name,new T.BufferAttribute(a,4));
    fitClipBounds();body=new T.Mesh(geom,material());body.frustumCulled=false;scene.add(body);$('source').src=DATA+e.source;$('source-info').textContent=`${e.player} · ${e.hand}-handed · source starts at saved frame ${e.source_start}`;
    $('seek').max=e.frames-1;$('frame-number').max=e.frames-1;$('events').replaceChildren();for(const c of e.audit.contacts){const b=document.createElement('button');b.textContent=`${c.kind} · ${c.frame}${c.impact_unverified?' · unverified':''}`;b.onclick=()=>{playing=false;$('source').pause();$('play').textContent='Play';const timing=e.balls.find(b=>b.frame===c.frame&&b.flight);const f=timing?timing.contact_seconds*e.fps:c.frame;draw(f,true);updateView(f);};$('events').append(b);}
    const a=e.audit;$('evidence').textContent=`Source racket-point error, median: ${a.median_point_error_before_px.toFixed(1)} → ${a.median_point_error_after_px.toFixed(1)} px. Grip is inferred, not measured. Axial hold: ${a.axial_sliding??"unchanged"}. Contact angles are shot-specific plausibility priors; source contact timing is uncertain. ${a.support_grasp?.enabled?'Two-handed strokes use an authored closed upper-handle grasp; exact bevel and fingers are inferred.':'Support uses the previous registration.'} Maximum added arm-reach mismatch: ${(a.support.max_added_reach_error_m*1000).toFixed(1)} mm. This is a motion review candidate, not certified reconstruction.`;
    draw(0,true);updateView(0);draw(0);$('status').dataset.testid='loaded-'+e.id;window.dispatchEvent(new Event('motion-loaded'));
  }catch(err){$('error').textContent=String(err);console.error(err);}
}
$('clip').onchange=()=>load($('clip').value);
$('play').onclick=async()=>{playing=!playing;$('play').textContent=playing?'Pause':'Play';if(!playing){$('source').pause();return;}if(frame>=entry.frames-1)draw(0,true);$('source').currentTime=(entry.source_start+frame+.001)/entry.source_fps;$('source').playbackRate=entry.fps/entry.source_fps*+$('speed').value;try{await $('source').play();}catch(err){playing=false;$('play').textContent='Play';$('error').textContent='Source playback failed: '+err;}};
$('go-frame').onclick=$('frame-number').onchange=()=>{playing=false;$('source').pause();$('play').textContent='Play';draw(+$('frame-number').value,true);};
$('frame-number').onfocus=()=>{playing=false;$('source').pause();$('play').textContent='Play';};
$('frame-number').onkeydown=e=>{if(e.key==='Enter')$('go-frame').click();};
$('seek').oninput=()=>{playing=false;$('source').pause();$('play').textContent='Play';draw(+$('seek').value,true);};
for(const [id,step]of [['prev',-1],['next',1]])$(id).onclick=()=>{playing=false;$('source').pause();$('play').textContent='Play';draw(Math.floor(frame)+step,true);};
for(const [id,m]of [['baseline','old'],['candidate','new']])$(id).onclick=()=>{mode=m;$('baseline').setAttribute('aria-pressed',mode==='old');$('candidate').setAttribute('aria-pressed',mode==='new');draw(frame,true);};
for(const b of $('cameras').querySelectorAll('button'))b.onclick=()=>{view=b.dataset.view;for(const p of $('cameras').querySelectorAll('button'))p.setAttribute('aria-pressed',p===b);updateView(frame);draw(frame);};
$('full-source').onchange=()=>{paintSource();if(view==='source')updateView(frame);};
for(const id of ['ball','ghost'])$(id).onchange=()=>draw(frame);$('speed').onchange=()=>{if(entry)$('source').playbackRate=entry.fps/entry.source_fps*+$('speed').value;};
new ResizeObserver(()=>{renderer.setSize(stage.clientWidth,stage.clientHeight);camera.aspect=stage.clientWidth/stage.clientHeight;camera.updateProjectionMatrix();if(entry)updateView(frame);draw(frame);}).observe(stage);
function tick(now){requestAnimationFrame(tick);if(playing&&entry){let f=$('source').currentTime*entry.source_fps-entry.source_start;if(f>=entry.frames-1){if(LOOP){f=0;$('source').currentTime=(entry.source_start+.001)/entry.source_fps;}else{playing=false;$('source').pause();$('play').textContent='Play';f=entry.frames-1;}}draw(f,false);paintSource();}renderer.render(scene,camera);}requestAnimationFrame(tick);
const manifest=await(await fetch(DATA+'manifest.json')).json();for(const e of manifest){const o=document.createElement('option');o.value=e.id;o.textContent=e.player.split('(')[0]+' · '+e.id+(e.diagnostic?' · diagnostic':'' );$('clip').append(o);}
const requested=params,wanted=requested.get('point')||requested.get('clip'),initial=manifest.find(e=>e.id===wanted)?.id||'djokovic-iw-a';await load(initial);
if(entry&&requested.has('frame'))draw(Number(requested.get('frame'))||0,true);
const cameraName=(requested.get('camera')||requested.get('view')||'').toLowerCase().replace(/[^a-z]/g,'');
const initialCamera=$('cameras').querySelector(`button[data-view="${CAMERA_ALIASES[cameraName]||cameraName}"]`);if(initialCamera)initialCamera.click();
if(LOOP&&entry){try{await $('source').play();$('source').pause();}catch(err){}$('play').click();}
