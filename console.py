#!/usr/bin/python3
"""This is the console for AirBnB"""

import cmd
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review


class HBNBCommand(cmd.Cmd):

    """Class for the command interpreter."""

    prompt = "(hbnb) "
    __classes = {
            "BaseModel",
            "User",
            "State",
            "City",
            "Place",
            "Amenity",
            "Review"
            }

    def update_dict(self, classname, uid, s_dict):
        """Helper method for update() with a dictionary."""
        s = s_dict.replace("'", '"')
        d = json.loads(s)
        if not classname:
            print("** class name missing **")
        elif classname not in storage.classes():
            print("** class doesn't exist **")
        elif uid is None:
            print("** instance id missing **")
        else:
            key = "{}.{}".format(classname, uid)
            if key not in storage.all():
                print("** no instance found **")
            else:
                attributes = storage.attributes()[classname]
                for attribute, value in d.items():
                    if attribute in attributes:
                        value = attributes[attribute](value)
                    setattr(storage.all()[key], attribute, value)
                storage.all()[key].save()

    def precmd(self, arg):
        if any(char in arg for char in ['.', '(', ')']):
            arg = arg.replace('.', ' ').replace('(', ' ').replace(')', ' ')
            words = arg.split()
            if len(words) >= 2:
                words[0], words[1] = words[1], words[0]
            new_arg = ' '.join(words)
        else:
            new_arg = arg
        return super().precmd(new_arg)

    def do_create(self, arg):
        """Usage: create <class>
        Create a new class instance and print its id.
        """
        if arg:
            class_name = arg.strip()
            if class_name in HBNBCommand.__classes:
                instance = eval(class_name)().id
                storage.save()
                print(instance)
            else:
                print("** class doesn't exist **")
        else:
            print("** class name missing **")

    def do_show(self, arg):
        """Usage: show <class> <id> or <class>.show(<id>)
        Display the string representation of a class instance of a given id.
        """
        if arg:
            args_list = arg.split()
            class_name = args_list[0]
            if class_name not in HBNBCommand.__classes:
                print("** class doesn't exist **")
                return
            if len(args_list) >= 2:
                instance_id = args_list[1]
                objdict = storage.all()
                key = class_name + "." + instance_id
                if key not in objdict:
                    print("** no instance found **")
                else:
                    print(objdict[key])
            else:
                print("** instance id missing **")
        else:
            print("** class name missing **")

    def do_destroy(self, arg):
        """Usage: destroy <class> <id> or <class>.destroy(<id>)
        Delete a class instance of a given id."""
        if arg:
            args_list = arg.split()
            class_name = args_list[0]
            if class_name in HBNBCommand.__classes:
                if len(args_list) >= 2:
                    instance_id = args_list[1]
                    objdict = storage.all()
                    key = class_name + "." + instance_id
                    if key in objdict:
                        del objdict[key]
                        storage.save()
                    else:
                        print("** no instance found **")
                else:
                    print("** instance id missing **")
            else:
                print("** class doesn't exist **")
        else:
            print("** class name missing **")

    def do_all(self, line):
        """Prints all string representation of all instances.
        """
        if line != "":
            words = line.split(' ')
            if words[0] not in storage.classes():
                print("** class doesn't exist **")
            else:
                nl = [str(obj) for key, obj in storage.all().items()
                      if type(obj).__name__ == words[0]]
                print(nl)
        else:
            new_list = [str(obj) for key, obj in storage.all().items()]
            print(new_list)
    
    def do_count(self, line):
        """Counts the instances of a class.
        """
        words = line.split(' ')
        if not words[0]:
            print("** class name missing **")
        elif words[0] not in storage.classes():
            print("** class doesn't exist **")
        else:
            matches = [
                k for k in storage.all() if k.startswith(
                    words[0] + '.')]
            print(len(matches))

    def do_update(self, arg):
        """Usage: update <class> <id> <attribute_name> <attribute_value> or
       <class>.update(<id>, <attribute_name>, <attribute_value>) or
       <class>.update(<id>, <dictionary>)
        Update a class instance of a given id by adding or updating
        a given attribute key/value pair or dictionary."""
        args_list = arg.split()
        Obj_dict = storage.all()
        if len(args_list) == 0:
            print("** class name missing **")
            return False
        if args_list[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return False
        if len(args_list) == 1:
            print("** instance id missing **")
            return False
        if "{}.{}".format(args_list[0], args_list[1]) not in Obj_dict.keys():
            print("** no instance found **")
            return False
        if len(args_list) == 2:
            print("** attribute name missing **")
            return False
        if len(args_list) == 3:
            try:
                type(eval(argl[2])) != dict
            except NameError:
                print("** value missing **")
                return False
        if len(args_list) == 4:
            obj_instance = Obj_dict["{}.{}".format(args_list[0], args_list[1])]
            if args_list[2] in obj_instance.__class__.__dict__.keys():
                valtype = type(obj_instance.__class__.__dict__[args_list[2]])
                obj_instance.__dict__[args_list[2]] = valtype(args_list[3])
            else:
                obj_instance.__dict__[args_list[2]] = args_list[3]
        elif type(eval(args_list[2])) == dict:
            obj_instance = Obj_dict["{}.{}".format(args_list[0], args_list[1])]
            for k, v in eval(args_list[2]).items():
                if (k in obj_instance.__class__.__dict__.keys() and
                        type(obj_instance.__class__.__dict__[k]) in
                        {str, int, float}):
                    valtype = type(obj_instance.__class__.__dict__[k])
                    obj_instance.__dict__[k] = valtype(v)
                else:
                    obj_instance.__dict__[k] = v
        storage.save()

    def do_quit(self, arg):
        """Quit command to exit the program"""
        return True

    def do_EOF(self, arg):
        """Exit the program on Ctrl+D (EOF)"""
        print()
        return True

    def do_help(self, arg):
        """Show help information"""
        super().do_help(arg)

    def emptyline(self):
        """Do nothing when an empty line is entered"""
        pass


if __name__ == "__main__":
    HBNBCommand().cmdloop()
