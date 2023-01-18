
from ansys.mechanical.core.embedding import loader

def __initialize_runtime_pythonnet_3():
    import Python.Runtime.Codecs as codecs
    codecs.ListDecoder.Instance.Register()
    codecs.SequenceDecoder.Instance.Register()
    codecs.IterableDecoder.Instance.Register()
    # TODO - FunctionCodec

def initialize(version: int) -> None:
    if loader.is_pythonnet_3():
        __initialize_runtime_pythonnet_3()
    else:
        # pythonnet 2.5 is supported with some codecs
        # and some additions to the system path that are shipped with Mechanical in 2023 R1
        # these additions to the system path may not be desirable for pymechanical embedding
        if version == 231:
            import clr
            clr.AddReference("Ansys.Mechanical.CPython")
            import Ansys

            Ansys.Mechanical.CPython.CPythonEngine.InitializeRuntime()