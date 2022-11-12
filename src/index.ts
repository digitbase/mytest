
console.log('index');

function pr(input:any, type2?:number):void{
	console.log(typeof input, "==>",input);let _type = type2?type2:0;let str = ""
	if (_type > 0) {for(let i=0; i < 20; i++)  str +=_type.toString();console.log(`==============    ${str}    ===============`)}
}




function buildLabel(name: string): string {
  return buildLabel.prefix + name + buildLabel.suffix; //可访问合并中的命名空间中的属性
}

namespace buildLabel {
  export let suffix = "";
  export let prefix = "Hello, ";
}


pr(buildLabel("Sam Smith"));

pr('test1')