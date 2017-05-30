#include <wchar.h>
#ifdef _DEBUG
#undef _DEBUG
#include <python.h>
#define _DEBUG
#else
#include <python.h>
#endif
#include <Windows.h>
#include <Shlwapi.h>

void get_base_path(wchar_t* base_path)
{
	GetModuleFileName(nullptr, base_path, MAX_PATH);
	PathRemoveFileSpec(base_path);
}

wchar_t** convert_args(int argc, char** argv)
{
	wchar_t** _argv = static_cast<wchar_t **>(calloc(argc, sizeof(wchar_t *)));

	for (int i = 0; i < argc; i++)
	{
		int len = strlen(argv[i]);
		_argv[i] = static_cast<wchar_t*>(calloc(len + 1, sizeof(wchar_t)));
		mbstowcs(_argv[i], argv[i], len);
	}

	return _argv;
}

void initialize_python(wchar_t* base_path, int argc, wchar_t** _argv)
{
	wchar_t python_zip[MAX_PATH];
	wcscpy(python_zip, base_path);
	wcsncat(python_zip, L"\\python.zip", MAX_PATH);

	Py_SetProgramName(_argv[0]);
	Py_SetPath(python_zip);
	Py_InitializeEx(0);
	PySys_SetArgv(argc, _argv);
}

void append_path(PyObject *sys_path, wchar_t* base_path, wchar_t* name)
{
	wchar_t dir[MAX_PATH];
	wcscpy(dir, base_path);
	wcsncat(dir, L"\\", MAX_PATH);
	wcsncat(dir, name, MAX_PATH);

	PyObject* python_path = PyUnicode_FromWideChar(dir, -1);
	PyList_Append(sys_path, python_path);
	Py_DECREF(python_path);
}

void fill_sys_path(wchar_t* base_path, bool plugin)
{
	PyObject *sys_path = PySys_GetObject("path");

	PySequence_DelSlice(sys_path, 0, PySequence_Length(sys_path));
	append_path(sys_path, base_path, L"python.zip");
	append_path(sys_path, base_path, L"dlls");
	append_path(sys_path, base_path, L"sp.zip");
	if (plugin)
	{
		append_path(sys_path, base_path, L"pl_runner.zip");
	}
	else
	{
		append_path(sys_path, base_path, L"umlfri.zip");
	}
}

void finalize_python()
{
	Py_Finalize();
}

void free_args(int argc, wchar_t** _argv)
{
	for (int i = 0; i < argc; i++) {
		free(_argv[i]);
	}

	free(_argv);
}

void common_main(int argc, wchar_t** argv, bool console)
{
	wchar_t base_path[MAX_PATH];

	get_base_path(base_path);

	initialize_python(base_path, argc, argv);

	fill_sys_path(base_path, false);

	int exc = PyRun_SimpleString("import sys; from umlfri2.qtgui import qt_main; sys.exit(qt_main(sys.argv))");

	if (exc < 0)
	{
		if (console) {
			printf("\n\nError occured. Press ENTER to continue.");
			getchar();
		} else {
			MessageBox(nullptr, L"Error occured.", L"An error occured while running the UML .FRI app.", MB_OK);
		}
	}

	finalize_python();

	free_args(argc, argv);
}


int main(int argc, char** argv)
{
	wchar_t** _argv = convert_args(argc, argv);

	common_main(argc, _argv, false);
}

int CALLBACK WinMain(
	_In_ HINSTANCE hInstance,
	_In_ HINSTANCE hPrevInstance,
	_In_ LPSTR     lpCmdLine,
	_In_ int       nCmdShow
)
{
	int argc;
	wchar_t** _argv = CommandLineToArgvW(GetCommandLineW(), &argc);

	common_main(argc, _argv, false);
}