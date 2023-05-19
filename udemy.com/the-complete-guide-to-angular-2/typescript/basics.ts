// types
let age: number = 10;
age = 10;

let name1: string;

let hobbies: string[] = ['abc', 'def'];

let person: { 
	name: string;
	age:number;
};

person = {
	name: 'max',
	age: 20
};

let people: { 
	name: string;
	age:number;
}[];

let course = 'typescript';
// course = 10; // invalid due to type inference

let course2 : string | number = 'typescript';
course2 = 10;

// type definition
type Person = {
	name: 'max';
	age: 20;
};
let persons: Person[];

// return type infered
function add(a: number, b: number) {
	return a+b;
}

// return type void
function log(msg: number) {
	console.log(msg);
}

function insertAtBeginningUnsafe(array: any[], value: any) {
	const newArray = [value, ...array];
	return newArray;
}

// Generics

function insertAtBeginning<T>(array: T[], value: T) {
	const newArray = [value, ...array];
	return newArray;
}

// Classes

class Student {
	name: string;
	private courses: string[];

	constructor(name: string) {
		this.name = name;
	}
   	enroll(course: string) {
   		this.courses.push(course);
   	}
   	listcourses() {
   		return this.courses.slice();
   	}

}

interface Human {
	name: string;
	greet(): void;
}

class Teacher implements Human {
	name: string;
	greet() {
		console.log('hello');
	}
}

let max: Human;

max = {
	name: 'Max',
	greet() {
		console.log('hello');
	}
}

