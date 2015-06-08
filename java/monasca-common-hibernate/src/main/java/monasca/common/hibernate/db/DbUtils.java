/*
 * Copyright 2015 FUJITSU LIMITED
 *
 * Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except
 * in compliance with the License. You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software distributed under the License
 * is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
 * or implied. See the License for the specific language governing permissions and limitations under
 * the License.
 */
package monasca.common.hibernate.db;

import java.nio.ByteBuffer;
import java.util.UUID;

class DbUtils {

  final static byte[] DEFAULT_VALUE = new byte[20];

  static final byte[] toByteArray(UUID uuid) {
    ByteBuffer bb = ByteBuffer.wrap(new byte[16]);
    bb.putLong(uuid.getMostSignificantBits()); // order is important here!
    bb.putLong(uuid.getLeastSignificantBits());
    return bb.array();
  }

  static final UUID toUUID(byte[] byteArray) {
    byte[] tmp = DEFAULT_VALUE.clone();
    System.arraycopy(byteArray, 0, tmp, 0, byteArray.length);
    ByteBuffer bb = ByteBuffer.wrap(tmp);
    long high = bb.getLong();
    long low = bb.getLong();
    UUID uuid = new UUID(high, low);
    return uuid;
  }
}
