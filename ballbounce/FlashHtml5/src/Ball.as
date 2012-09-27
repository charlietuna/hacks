package
{
	import com.cb.utils.FrameRateCounter;
	
	import flash.display.Shape;
	import flash.display.Sprite;
	import flash.events.Event;
	import flash.events.TimerEvent;
	import flash.utils.Timer;
	
	[SWF(pageTitle="Ball", backgroundColor="#FFFFFF", frameRate="60", width="500", height="500")]	
	public class Ball extends Sprite
	{
		private var ball:Shape;
		private var canvas:Sprite;
		private var timer:Timer;
		private var y2:int = 250;
		private var x2:int = 250;
		private var vspeed:Number = 0;
		
		public function Ball()
		{
			
			canvas = new Sprite();
			ball = new Shape();
			this.addChild(canvas);
			canvas.addChild(ball);
			
			stage.addEventListener(Event.ENTER_FRAME, ballLoop);
		}
		
		private function ballLoop(e:Event):void
		{
			
			if ((y2==500-32-20)) {
				vspeed = -10;
			}
			y2 = y2+vspeed;
			
			if (y2<500-32-20) {
				vspeed += .5;
			}else{
				vspeed = 0;
			}
			
			if (y2>500-32-20) {
				y2=500-32-20;
			}
			ball.graphics.clear();
			ball.graphics.beginFill(0xFFFFFF);
			ball.graphics.drawRect(0, 0, 500, 500);
			ball.graphics.beginFill(0x000000);
			ball.graphics.drawCircle(x2, y2,20);
			ball.graphics.beginFill(0x00FF00);
			ball.graphics.drawRect(0, 500-32, 500, 32);
		}
	}
}