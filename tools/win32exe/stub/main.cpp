#include <wchar.h>
#include <Python.h>
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

int main(int argc, char** argv)
{
	HWND console = GetConsoleWindow();
	ShowWindow(console, SW_HIDE);

	wchar_t base_path[MAX_PATH];

	get_base_path(base_path);

	wchar_t** _argv = convert_args(argc, argv);

	initialize_python(base_path, argc, _argv);

	fill_sys_path(base_path, false);

	int exc = PyRun_SimpleString("import sys; import main; sys.exit(main.main(sys.argv))");

	if (exc < 0)
	{
		ShowWindow(console, SW_SHOW);
		printf("\n\nError occured. Press ENTER to continue.");
		getchar();
	}

	finalize_python();

	free_args(argc, _argv);
}
