import unittest

from itblib.components import ComponentAcceptor, TransformComponent


class TestTransformComponentMethods(unittest.TestCase):
    def setUp(self) -> None:
        self.acceptor_a = ComponentAcceptor()
        self.acceptor_b = ComponentAcceptor()
        self.transform_component_a = TransformComponent()
        self.transform_component_b = TransformComponent()

    def test_attach_and_remove(self):
        self.assertIsNone(self.acceptor_a.get_component(TransformComponent))
        self.transform_component_a.attach_component(self.acceptor_a)
        self.assertIsInstance(self.acceptor_a.get_component(TransformComponent), TransformComponent)
        self.transform_component_a.detach_component()
        self.assertIsNone(self.acceptor_a.get_component(TransformComponent))

    def test_transform_target(self):
        default_pos = (0,  0)
        move_pos = (15, -10)
        self.transform_component_a.attach_component(self.acceptor_a)
        self.transform_component_b.attach_component(self.acceptor_b)
        self.transform_component_b.set_transform_target(self.acceptor_a)
        self.assertEqual(self.transform_component_a.get_position(), default_pos)
        self.assertEqual(self.transform_component_b.get_position(), default_pos)
        self.transform_component_a.relative_position = move_pos
        self.assertEqual(self.transform_component_a.get_position(), move_pos)
        self.assertEqual(self.transform_component_b.get_position(), move_pos)
