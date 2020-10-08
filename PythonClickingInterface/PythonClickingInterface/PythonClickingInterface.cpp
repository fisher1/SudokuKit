// PythonClickingInterface.cpp : Defines the exported functions for the DLL application.
//

#include "stdafx.h"

#include <Windows.h>
#include <cmath>
#include <iostream>

extern "C" __declspec(dllexport) void MouseTo(int x, int y) {
	RECT desktop_rect;
	GetClientRect(GetDesktopWindow(), &desktop_rect);
	INPUT input = { 0 };
	input.type = INPUT_MOUSE;
	input.mi.dwFlags =
		MOUSEEVENTF_ABSOLUTE | MOUSEEVENTF_VIRTUALDESK | MOUSEEVENTF_MOVE;
	input.mi.dx = x * 65536 / desktop_rect.right;
	input.mi.dy = y * 65536 / desktop_rect.bottom;
	SendInput(1, &input, sizeof(input));
}

void MouseLButton(bool tf_down_up) {
	INPUT input = { 0 };
	input.type = INPUT_MOUSE;
	input.mi.dwFlags = tf_down_up ? MOUSEEVENTF_LEFTDOWN : MOUSEEVENTF_LEFTUP;
	SendInput(1, &input, sizeof(input));
}

extern "C" __declspec(dllexport) void MouseLClick() {
	MouseLButton(true);
	MouseLButton(false);
}

void ClickNTimes() {
	const int ITEMS_COUNT = 49;
	for (int i = 0; i < ITEMS_COUNT; ++i) {
		MouseLClick();
		Sleep(50);
	}
}

extern "C" __declspec(dllexport) void PressKBKey(int key) {
	INPUT input = { 0 };
	input.type = INPUT_KEYBOARD;
	input.ki.wVk = 0x30 + key;
	SendInput(1, &input, sizeof(input));
}
