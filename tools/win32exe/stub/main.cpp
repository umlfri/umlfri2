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

#define MAX_SYSTEM_PATH 10000

void get_base_path(wchar_t* base_path)
{
	GetModuleFileName(nullptr, base_path, MAX_PATH);
	PathRemoveFileSpec(base_path);
#ifdef _DEBUG
	printf("* Base path is: %ls\n", base_path);
#endif
}

wchar_t** convert_args(int argc, char** argv)
{
	wchar_t** _argv = static_cast<wchar_t **>(calloc(argc, sizeof(wchar_t *)));

#ifdef _DEBUG
	printf("* Argument count: %d\n", argc);
#endif

	for (int i = 0; i < argc; i++)
	{
		int len = strlen(argv[i]);
		_argv[i] = static_cast<wchar_t*>(calloc(len + 1, sizeof(wchar_t)));
		mbstowcs(_argv[i], argv[i], len);
#ifdef _DEBUG
		printf("* Argument[%d]: %ls\n", i, _argv[i]);
#endif
	}

	return _argv;
}

void initialize_python(wchar_t* base_path, int argc, wchar_t** _argv)
{
	wchar_t python_zip[MAX_PATH];
	wcscpy(python_zip, base_path);
	wcsncat(python_zip, L"\\python.zip", MAX_PATH);

#ifndef _DEBUG
	Py_OptimizeFlag = 2;
#endif

	Py_SetProgramName(_argv[0]);
	Py_SetPath(python_zip);
	Py_InitializeEx(0);
	PySys_SetArgv(argc, _argv);

	// mark as frozen
	PySys_SetObject("frozen", Py_True);
#ifdef _DEBUG
	printf("* Python initialized correctly\n");
#endif
}

void append_path(PyObject *sys_path, wchar_t* base_path, wchar_t* name)
{
	wchar_t dir[MAX_PATH];
	wcscpy(dir, base_path);
	if (name != nullptr)
	{
		wcsncat(dir, L"\\", MAX_PATH);
		wcsncat(dir, name, MAX_PATH);
	}

	PyObject* python_path = PyUnicode_FromWideChar(dir, -1);
	PyList_Append(sys_path, python_path);
	Py_DECREF(python_path);

#ifdef _DEBUG
	printf("* sys.path extended by: %ls\n", dir);
#endif
}

bool is_plugin(int argc, wchar_t** argv)
{
	bool plugin = false;

	if (argc == 2 && wcscmp(argv[1], L"--plugin") == 0)
		plugin = true;

#ifdef _DEBUG
	if (plugin)
		printf("* Started as plugin\n");
	else
		printf("* Started as main app\n");
#endif

	return plugin;
}

void fill_sys_path(wchar_t* base_path, bool plugin)
{
	PyObject *sys_path = PySys_GetObject("path");

	PySequence_DelSlice(sys_path, 0, PySequence_Length(sys_path));
	append_path(sys_path, base_path, nullptr);
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

void add_to_system_path(wchar_t *base_path)
{
	wchar_t new_system_path[MAX_SYSTEM_PATH];

	wchar_t old_system_path[MAX_SYSTEM_PATH];
	size_t old_size;
	old_size = MAX_SYSTEM_PATH;
	_wgetenv_s(&old_size, old_system_path, MAX_SYSTEM_PATH, L"PATH");

	wcscpy(new_system_path, base_path);
	wcsncat(new_system_path, L";", MAX_SYSTEM_PATH);
	wcsncat(new_system_path, old_system_path, MAX_SYSTEM_PATH);

	_wputenv_s(L"PATH", new_system_path);

#ifdef _DEBUG
	printf("* New PATH: %ls\n", new_system_path);
#endif
}

bool run(const char *code)
{
#ifdef _DEBUG
	printf("Executing: %s\n", code);
#endif

	int exc = PyRun_SimpleString(code);

#ifdef _DEBUG
	printf("* Exception no: %d\n", exc);
#endif

	return exc < 0;
}

bool run(bool plugin)
{
	if (plugin)
		return run("import sys; from python_runner import main; sys.exit(main(sys.argv))");
	else
		return run("import sys; from umlfri2.qtgui import qt_main; sys.exit(qt_main(sys.argv))");
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

	add_to_system_path(base_path);

	initialize_python(base_path, argc, argv);

	bool plugin = is_plugin(argc, argv);

	fill_sys_path(base_path, plugin);

	bool was_exc = run(plugin);

	if (was_exc)
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

	common_main(argc, _argv, true);
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